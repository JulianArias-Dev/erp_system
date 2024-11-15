from pydantic import BaseModel

# Esquema para crear un producto
class ProductCreate(BaseModel):
    code: str
    name: str
    unit_price: float
    available_units: int
    max_capacity: int

# Esquema para devolver un producto
class ProductResponse(BaseModel):
    id: int
    code: str
    name: str
    unit_price: float
    available_units: int
    max_capacity: int

    class Config:
        orm_mode = True
