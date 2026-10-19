
from app.repositories.restaurant_repository import RestaurantRepository
from app.domain.models import Restaurant
from app.domain.schemas import RestaurantCreate, RestaurantUpdate


class RestaurantService:
    """Contiene la lógica de negocio de los restaurantes."""

    def __init__(self):
        self.repository = RestaurantRepository()

    def create_restaurant(
        self,
        data: RestaurantCreate,
    ) -> Restaurant:
        return self.repository.create(data)

    def list_restaurants(
        self,
        city: str | None = None,
        category: str | None = None,
        price: int | None = None,
        order_by: str = "name",
        direction: str = "asc",
        limit: int = 20,
        offset: int = 0,
    ) -> list[Restaurant]:
        return self.repository.list(
            city=city,
            category=category,
            price=price,
            order_by=order_by,
            direction=direction,
            limit=limit,
            offset=offset,
        )

    def get_restaurant(self, restaurant_id: str) -> Restaurant | None:
        return self.repository.get_by_id(restaurant_id)

    def update_restaurant(
        self,
        restaurant_id: str,
        data: RestaurantUpdate,
    ) -> Restaurant | None:
        return self.repository.update(restaurant_id, data)

    def delete_restaurant(self, restaurant_id: str) -> bool:
        return self.repository.delete(restaurant_id)
