from sqlalchemy import Column, Integer, String, Float
from app.config import Base

class Product(Base):
    __tablename__ = "products"

    id_product = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    unit_price = Column(Float, nullable=False)
