from pydantic import BaseModel

# Esquema para crear un ingrediente
class PurchaseIngredientCreate(BaseModel):
    supplier_id: int
    ingredient_id: int
    quantity: float
    value : float