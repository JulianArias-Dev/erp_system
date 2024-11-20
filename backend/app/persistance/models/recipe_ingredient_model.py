from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.config import Base

class RecipeIngredients(Base): 
    __tablename__ = 'recipe_ingredients'
    
    fk_recipe = Column(Integer, ForeignKey('recipe.id'), primary_key=True)
    fk_ingredient = Column(Integer, ForeignKey('ingredients.id'), primary_key=True)
    quantity = Column(Integer, nullable=False)

    # Relación con Ingredient
    ingredient = relationship("Ingredient", backref="recipe_ingredients")
    # Relación con Recipe
    recipe = relationship("Recipe", back_populates="ingredients")
