from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.config import Base

class Recipe(Base):
    __tablename__ = 'recipe'

    id = Column(Integer, primary_key=True, index=True)
    fk_product = Column(Integer, ForeignKey('products.id'), nullable=False)
    preparation_time = Column(Integer, nullable=False)
    
    # Relación con Product
    product = relationship("Product", back_populates="recipe")
    # Relación con RecipeIngredients
    ingredients = relationship("RecipeIngredients", back_populates="recipe")
