from pydantic import BaseModel, Field
from typing import List

# Esquema para los ingredientes en una receta
class RecipeIngredientBase(BaseModel):
    id: int = Field(..., description="ID del ingrediente")
    quantity: float = Field(..., description="Cantidad requerida del ingrediente")

# Esquema para crear una receta
class RecipeCreate(BaseModel):
    product_id: int = Field(..., description="ID del producto asociado a la receta")
    preparation_time: int = Field(..., description="Tiempo de preparación en minutos")
    ingredients: List[RecipeIngredientBase] = Field(
        ..., description="Lista de ingredientes con sus cantidades"
    )

# Esquema para la respuesta de una receta
class RecipeResponse(BaseModel):
    id: int
    preparation_time: int
    product: dict
    ingredients: List[dict]

    class Config:
        orm_mode = True
