from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.config import Base

class Product(Base):
   __tablename__ = "products"

   id = Column(Integer, primary_key=True, index=True)
   code = Column(String(50), unique=True, nullable=False)  
   name = Column(String(255), nullable=False)
   unit_price = Column(Float, nullable=False)
   available_units = Column(Integer, nullable=False)
   max_capacity = Column(Integer, nullable=False)

   # Relación con Recipe
   recipe = relationship("Recipe", back_populates="product")
