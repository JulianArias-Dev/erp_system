from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.config import Base

class SupplierIngredient(Base):
    __tablename__ = "supplier_ingredients"

    fk_supplier = Column(Integer, ForeignKey("suppliers.id"), primary_key=True)
    fk_ingredient = Column(Integer, ForeignKey("ingredients.id"), primary_key=True)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    # Relaciones con Supplier e Ingredient
    supplier = relationship("Supplier", back_populates="ingredients")
    ingredient = relationship("Ingredient", back_populates="supplier")
