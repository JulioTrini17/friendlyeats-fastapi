
import sys
from pathlib import Path

# Obtener la carpeta principal del proyecto.
ROOT_DIR = Path(__file__).resolve().parent.parent

# Permitir que Python encuentre el paquete app.
sys.path.insert(0, str(ROOT_DIR))

# Importar Firestore después de configurar la ruta.
from app.core.firebase import db


restaurantes = [
    {
        "id": "seed-01",
        "name": "La Casa del Sabor",
        "category": "Mexicana",
        "city": "Puebla",
        "price": 2,
        "photoUrl": None,
        "avgRating": 4.6,
        "numRatings": 42,
    },
    {
        "id": "seed-02",
        "name": "Tacos El Buen Pastor",
        "category": "Mexicana",
        "city": "Puebla",
        "price": 1,
        "photoUrl": None,
        "avgRating": 4.8,
        "numRatings": 65,
    },
    {
        "id": "seed-03",
        "name": "Pasta Roma",
        "category": "Italiana",
        "city": "Cholula",
        "price": 3,
        "photoUrl": None,
        "avgRating": 4.4,
        "numRatings": 28,
    },
    {
        "id": "seed-04",
        "name": "Sushi Sakura",
        "category": "Japonesa",
        "city": "Puebla",
        "price": 3,
        "photoUrl": None,
        "avgRating": 4.7,
        "numRatings": 51,
    },
    {
        "id": "seed-05",
        "name": "Hamburguesas Central",
        "category": "Americana",
        "city": "Atlixco",
        "price": 2,
        "photoUrl": None,
        "avgRating": 4.2,
        "numRatings": 19,
    },
    {
        "id": "seed-06",
        "name": "Verde Natural",
        "category": "Saludable",
        "city": "Cholula",
        "price": 2,
        "photoUrl": None,
        "avgRating": 4.5,
        "numRatings": 33,
    },
    {
        "id": "seed-07",
        "name": "El Rincón Italiano",
        "category": "Italiana",
        "city": "Puebla",
        "price": 3,
        "photoUrl": None,
        "avgRating": 4.3,
        "numRatings": 24,
    },
    {
        "id": "seed-08",
        "name": "Antojitos Lupita",
        "category": "Mexicana",
        "city": "Atlixco",
        "price": 1,
        "photoUrl": None,
        "avgRating": 4.9,
        "numRatings": 72,
    },
    {
        "id": "seed-09",
        "name": "Café de la Plaza",
        "category": "Cafetería",
        "city": "Cholula",
        "price": 2,
        "photoUrl": None,
        "avgRating": 4.1,
        "numRatings": 16,
    },
    {
        "id": "seed-10",
        "name": "Mariscos del Puerto",
        "category": "Mariscos",
        "city": "Puebla",
        "price": 3,
        "photoUrl": None,
        "avgRating": 4.6,
        "numRatings": 37,
    },
]


def cargar_restaurantes():
    for restaurante in restaurantes:
        restaurant_id = restaurante["id"]

        datos = {
            key: value
            for key, value in restaurante.items()
            if key != "id"
        }

        db.collection("restaurants").document(restaurant_id).set(datos)

        print(
            "Restaurante guardado: "
            + datos["name"]
            + " ("
            + restaurant_id
            + ")"
        )

    print("\nCarga inicial terminada: 10 restaurantes procesados.")


if __name__ == "__main__":
    cargar_restaurantes()
