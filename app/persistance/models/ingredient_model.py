from sqlalchemy import Column, Integer, String
from app.config import Base
from sqlalchemy.orm import relationship

class Ingredient(Base):
    __tablename__ = 'ingredients'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    code = Column(String(50), unique=True, nullable=False)  
    available_units = Column(Integer, nullable=False)
    max_capacity = Column(Integer, nullable=False)
    type = Column(String(50), nullable=False)
    
    # Relación con SupplierIngredient
    supplier = relationship("SupplierIngredient", back_populates="ingredient")

