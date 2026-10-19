
from google.cloud.firestore_v1.base_query import FieldFilter

from app.core.firebase import db
from app.domain.models import Restaurant
from app.domain.schemas import RestaurantCreate, RestaurantUpdate


class RestaurantRepository:
    """Administra los restaurantes almacenados en Firestore."""

    COLLECTION = "restaurants"

    def __init__(self):
        self.collection = db.collection(self.COLLECTION)

    def create(self, data: RestaurantCreate) -> Restaurant:
        """Crea un restaurante y devuelve el registro guardado."""

        document = self.collection.document()
        restaurant_data = data.model_dump(mode="json")

        document.set(restaurant_data)

        return Restaurant(
            id=document.id,
            **restaurant_data,
        )

    def list(
        self,
        city: str | None = None,
        category: str | None = None,
        price: int | None = None,
        order_by: str = "name",
        direction: str = "asc",
        limit: int = 20,
        offset: int = 0,
    ) -> list[Restaurant]:
        """Lista restaurantes con filtros, orden y paginación."""

        query = self.collection

        if city:
            query = query.where(
                filter=FieldFilter("city", "==", city)
            )

        if category:
            query = query.where(
                filter=FieldFilter("category", "==", category)
            )

        if price is not None:
            query = query.where(
                filter=FieldFilter("price", "==", price)
            )

        if order_by not in ("name", "avgRating"):
            order_by = "name"

        if direction.lower() not in ("asc", "desc"):
            direction = "asc"

        query = query.order_by(
            order_by,
            direction=(
                "DESCENDING" if direction.lower() == "desc"
                else "ASCENDING"
            ),
        )

        query = query.offset(max(offset, 0)).limit(
            min(max(limit, 1), 100)
        )

        restaurants = []

        for document in query.stream():
            restaurant_data = document.to_dict()

            restaurants.append(
                Restaurant(
                    id=document.id,
                    **restaurant_data,
                )
            )

        return restaurants

    def get_by_id(self, restaurant_id: str) -> Restaurant | None:
        """Busca un restaurante por su identificador."""

        document = self.collection.document(restaurant_id).get()

        if not document.exists:
            return None

        return Restaurant(
            id=document.id,
            **document.to_dict(),
        )

    def update(
        self,
        restaurant_id: str,
        data: RestaurantUpdate,
    ) -> Restaurant | None:
        """Actualiza únicamente los campos enviados."""

        document = self.collection.document(restaurant_id)
        snapshot = document.get()

        if not snapshot.exists:
            return None

        changes = data.model_dump(
            mode="json",
            exclude_unset=True,
        )

        if changes:
            document.update(changes)

        updated = document.get()

        return Restaurant(
            id=updated.id,
            **updated.to_dict(),
        )

    def delete(self, restaurant_id: str) -> bool:
        """Elimina un restaurante si existe."""

        document = self.collection.document(restaurant_id)

        if not document.get().exists:
            return False

        document.delete()
        return True
