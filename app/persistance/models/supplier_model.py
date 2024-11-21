from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.config import Base

class Supplier(Base):
    __tablename__ = "suppliers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    contact = Column(String(255), nullable=False)
    
    # Relación con SupplierIngredient
    ingredients = relationship("SupplierIngredient", back_populates="supplier")
