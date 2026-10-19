
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


@pytest.fixture
def restaurant_payload():
    identificador = uuid4().hex[:8]

    return {
        "name": "Restaurante Prueba " + identificador,
        "category": "Mexicana",
        "city": "Puebla",
        "price": 2,
    }


@pytest.fixture
def created_restaurant(restaurant_payload):
    response = client.post(
        "/api/v1/restaurants",
        json=restaurant_payload,
    )

    assert response.status_code == 201

    restaurant = response.json()

    yield restaurant

    # Limpiar el registro después de la prueba.
    client.delete("/api/v1/restaurants/" + restaurant["id"])


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_restaurant(restaurant_payload):
    response = client.post(
        "/api/v1/restaurants",
        json=restaurant_payload,
    )

    assert response.status_code == 201

    restaurant = response.json()

    assert restaurant["name"] == restaurant_payload["name"]
    assert restaurant["category"] == "Mexicana"
    assert restaurant["city"] == "Puebla"
    assert restaurant["price"] == 2
    assert restaurant["avgRating"] == 0
    assert restaurant["numRatings"] == 0

    # Eliminar el registro creado por esta prueba.
    client.delete("/api/v1/restaurants/" + restaurant["id"])


def test_list_restaurants(created_restaurant):
    response = client.get("/api/v1/restaurants")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

    ids = [restaurant["id"] for restaurant in response.json()]

    assert created_restaurant["id"] in ids


def test_get_restaurant(created_restaurant):
    restaurant_id = created_restaurant["id"]

    response = client.get(
        "/api/v1/restaurants/" + restaurant_id
    )

    assert response.status_code == 200
    assert response.json()["id"] == restaurant_id


def test_get_nonexistent_restaurant():
    response = client.get(
        "/api/v1/restaurants/identificador-inexistente-123"
    )

    assert response.status_code == 404


def test_update_restaurant(created_restaurant):
    restaurant_id = created_restaurant["id"]

    response = client.patch(
        "/api/v1/restaurants/" + restaurant_id,
        json={
            "name": "Restaurante Actualizado",
            "city": "Cholula",
        },
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Restaurante Actualizado"
    assert response.json()["city"] == "Cholula"


def test_delete_restaurant(restaurant_payload):
    create_response = client.post(
        "/api/v1/restaurants",
        json=restaurant_payload,
    )

    assert create_response.status_code == 201

    restaurant_id = create_response.json()["id"]

    delete_response = client.delete(
        "/api/v1/restaurants/" + restaurant_id
    )

    assert delete_response.status_code == 204

    get_response = client.get(
        "/api/v1/restaurants/" + restaurant_id
    )

    assert get_response.status_code == 404
