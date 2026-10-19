from pydantic import BaseModel, Field, ConfigDict


class Restaurant(BaseModel):
    """Representa un restaurante almacenado en Firestore."""

    model_config = ConfigDict(populate_by_name=True)

    id: str | None = None
    name: str
    category: str
    city: str
    price: int = Field(ge=1, le=3)
    photoUrl: str | None = None
    avgRating: float = Field(default=0, ge=0, le=5)
    numRatings: int = Field(default=0, ge=0)
