from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.persistance.models.ingredient_model import Ingredient
from app.domain.schemas.ingredient_schema import IngredientCreate, IngredientResponse

def create_ingredient(db:Session, ingredient:IngredientCreate):
    """Crea un ingrediente en la base de datos"""
    existing_ingredient = db.query(Ingredient).filter(Ingredient.code == ingredient.code).first()
    if existing_ingredient:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ingredient with this code already exists"
        )

    db_ingredient = Ingredient(
        name = ingredient.name,
        code = ingredient.code,
        available_units=ingredient.available_units,
        max_capacity=ingredient.max_capacity,
        type=ingredient.type,
    )
    db.add(db_ingredient)
    db.commit()
    db.refresh(db_ingredient)
    return {
        "message" : "Ingredient created succesfully!",
        "ingredient" : IngredientResponse.from_orm(db_ingredient),
        }
    
def get_ingredients(db: Session):
    """Obtiene todos los ingredientes."""
    return db.query(Ingredient).all()

def get_ingredient_by_code(db: Session, code: str):
    """Obtiene un ingrediente por su código."""
    return db.query(Ingredient).filter(Ingredient.code == code).first()

def update_ingredient(db: Session, id_ingredient: int, new_ingredient: IngredientCreate):
    """Actualiza los datos de un ingrediente existente."""
    ingredient = db.query(Ingredient).filter(Ingredient.id == id_ingredient).first()
    if not ingredient:
        return None
    ingredient.code = new_ingredient.code
    ingredient.name = new_ingredient.name
    ingredient.available_units = new_ingredient.available_units
    ingredient.max_capacity = new_ingredient.max_capacity
    ingredient.type=new_ingredient.type
    db.commit()
    db.refresh(ingredient)
    return {
        "message" : "Ingredient updated succesfully!",
        "ingredient" : IngredientResponse.from_orm(ingredient)
        }

def delete_ingredient(db: Session, id_ingredient: int):
    """Elimina un ingrediente por su ID."""
    ingredient = db.query(Ingredient).filter(Ingredient.id == id_ingredient).first()
    if not ingredient:
        return False
    db.delete(ingredient)
    db.commit()
    return True