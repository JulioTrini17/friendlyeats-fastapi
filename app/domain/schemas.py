
from pydantic import BaseModel, Field, ConfigDict, HttpUrl


class RestaurantCreate(BaseModel):
    """Datos obligatorios para registrar un restaurante."""

    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=2, max_length=100)
    category: str = Field(min_length=2, max_length=60)
    city: str = Field(min_length=2, max_length=80)
    price: int = Field(ge=1, le=3)
    photoUrl: HttpUrl | None = None


class RestaurantUpdate(BaseModel):
    """Campos que se pueden modificar parcialmente."""

    model_config = ConfigDict(str_strip_whitespace=True)

    name: str | None = Field(default=None, min_length=2, max_length=100)
    category: str | None = Field(default=None, min_length=2, max_length=60)
    city: str | None = Field(default=None, min_length=2, max_length=80)
    price: int | None = Field(default=None, ge=1, le=3)
    photoUrl: HttpUrl | None = None
