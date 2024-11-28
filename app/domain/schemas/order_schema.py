from pydantic import BaseModel, Field
from datetime import date

class OrderRegister(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0, description="La cantidad debe ser mayor a 0")
    date: date
