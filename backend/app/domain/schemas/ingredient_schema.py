from pydantic import BaseModel

# Esquema para crear un ingrediente
class IngredientCreate(BaseModel):
    name: str
    code: str
    available_units: float
    max_capacity: float
    type : str
    
# Esquema para devolver un ingrediente
class IngredientResponse(BaseModel):
    id: int
    name: str
    code: str
    available_units: int
    max_capacity: int
    type : str
    
    class Config:
        from_attributes = True