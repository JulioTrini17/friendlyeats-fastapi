
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.core.config import APP_NAME
from app.api.v1.restaurants import router as restaurants_router
from app.services.restaurant_service import RestaurantService

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "app" / "templates"

app = FastAPI(
    title=APP_NAME,
    description="API para administrar restaurantes de FriendlyEats.",
    version="1.0.0",
)

app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static",
)

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
service = RestaurantService()

# Mantener disponibles los endpoints de la API.
app.include_router(restaurants_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}


# Página principal.
@app.get("/")
def home(request: Request):
    restaurants = service.list_restaurants(limit=100)

    return templates.TemplateResponse(
        request=request,
        name="restaurants.html",
        context={
            "request": request,
            "app_name": APP_NAME,
            "restaurants": restaurants,
        },
    )


# IMPORTANTE: esta ruta debe ir antes de /restaurants/{restaurant_id}.
# Formulario para registrar un restaurante.
@app.get("/restaurants/new")
def restaurant_new(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="restaurant_form.html",
        context={
            "request": request,
            "app_name": APP_NAME,
            "restaurant": None,
        },
    )


# Formulario para editar un restaurante.
@app.get("/restaurants/{restaurant_id}/edit")
def restaurant_edit(request: Request, restaurant_id: str):
    restaurant = service.get_restaurant(restaurant_id)

    if restaurant is None:
        raise HTTPException(
            status_code=404,
            detail="Restaurante no encontrado",
        )

    return templates.TemplateResponse(
        request=request,
        name="restaurant_form.html",
        context={
            "request": request,
            "app_name": APP_NAME,
            "restaurant": restaurant,
        },
    )


# Detalle de un restaurante.
@app.get("/restaurants/{restaurant_id}")
def restaurant_detail(request: Request, restaurant_id: str):
    restaurant = service.get_restaurant(restaurant_id)

    if restaurant is None:
        raise HTTPException(
            status_code=404,
            detail="Restaurante no encontrado",
        )

    return templates.TemplateResponse(
        request=request,
        name="restaurant_detail.html",
        context={
            "request": request,
            "app_name": APP_NAME,
            "restaurant": restaurant,
        },
    )
