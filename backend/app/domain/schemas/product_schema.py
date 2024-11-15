from pydantic import BaseModel

class ProductCreate(BaseModel):
    code: str
    name: str
    unit_price: float

class ProductResponse(BaseModel):
    id_product: int
    code: str
    name: str
    unit_price: float

    class Config:
        orm_mode = True
