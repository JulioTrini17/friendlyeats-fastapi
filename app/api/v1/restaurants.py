
from fastapi import APIRouter, HTTPException, Query, Response, status

from app.domain.models import Restaurant
from app.domain.schemas import RestaurantCreate, RestaurantUpdate
from app.services.restaurant_service import RestaurantService


router = APIRouter(prefix="/api/v1/restaurants", tags=["Restaurantes"])
service = RestaurantService()


@router.post("", response_model=Restaurant, status_code=status.HTTP_201_CREATED)
def create_restaurant(data: RestaurantCreate):
    return service.create_restaurant(data)


@router.get("", response_model=list[Restaurant])
def list_restaurants(
    city: str | None = None,
    category: str | None = None,
    price: int | None = Query(default=None, ge=1, le=3),
    order_by: str = Query(default="name", pattern="^(name|avgRating)$"),
    direction: str = Query(default="asc", pattern="^(asc|desc)$"),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    return service.list_restaurants(
        city=city,
        category=category,
        price=price,
        order_by=order_by,
        direction=direction,
        limit=limit,
        offset=offset,
    )


@router.get("/{restaurant_id}", response_model=Restaurant)
def get_restaurant(restaurant_id: str):
    restaurant = service.get_restaurant(restaurant_id)

    if restaurant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurante no encontrado",
        )

    return restaurant


@router.patch("/{restaurant_id}", response_model=Restaurant)
def update_restaurant(restaurant_id: str, data: RestaurantUpdate):
    restaurant = service.update_restaurant(restaurant_id, data)

    if restaurant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurante no encontrado",
        )

    return restaurant


@router.delete("/{restaurant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_restaurant(restaurant_id: str):
    deleted = service.delete_restaurant(restaurant_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurante no encontrado",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
