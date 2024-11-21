from pydantic import BaseModel

class SupplierBase(BaseModel):
    name: str
    contact: str

class SupplierCreate(SupplierBase):
    pass

class SupplierUpdate(SupplierBase):
    pass

class SupplierIngredientResponse(BaseModel):
    ingredient_id: int
    ingredient_name: str
    quantity: int
    price: float

    class Config:
        from_attributes = True

class SupplierResponse(BaseModel):
    id: int
    name: str
    contact: str
    ingredients: list[SupplierIngredientResponse]

    class Config:
        from_attributes = True

class SupplierIngredientAdd(BaseModel):
    ingredient_id: int
    quantity: int
    price: float

class SupplierIngredientResponse(BaseModel):
    ingredient_id: int
    ingredient_name: str
    quantity: int
    price: float

    class Config:
        from_attributes = True