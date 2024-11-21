from sqlalchemy.orm import Session
from app.persistance.repository import ingredient_repository
from app.domain.schemas.ingredient_schema import IngredientCreate

def create_ingredient(db: Session, ingredient: IngredientCreate):
    """Crea un nuevo ingrediente."""
    ingredient = ingredient_repository.create_ingredient(db, ingredient)
    return {
        "id": ingredient.id,
        "code": ingredient.code,
        "name": ingredient.name,
        "available_units": ingredient.available_units,
        "max_capacity": ingredient.max_capacity,
        "type" : ingredient.type,
    }

def list_ingredients(db: Session):
    """Devuelve una lista de todos los ingredientes en formato JSON."""
    ingredients = ingredient_repository.get_ingredients(db)
    return [
        {
            "id": ingredient.id,
            "name": ingredient.name,
            "code": ingredient.code,
            "available_units": ingredient.available_units,
            "max_capacity": ingredient.max_capacity,
            "type": ingredient.type,
        }
        for ingredient in ingredients
    ]

def update_ingredient(db: Session, id_ingredient: int, new_ingredient: IngredientCreate):
    """Actualiza un ingrediente existente."""
    update_ingredient = ingredient_repository.update_ingredient(db, id_ingredient, new_ingredient)
    if update_ingredient :
        return {
            "id": update_ingredient.id,
            "name": update_ingredient.name,
            "code": update_ingredient.code,
            "available_units": update_ingredient.available_units,
            "max_capacity": update_ingredient.max_capacity,
            "type": update_ingredient.type,
        }
    return None

def delete_ingredient(db: Session, id_ingredient: int):
    """Elimina un ingrediente por su ID."""
    return ingredient_repository.delete_ingredient(db, id_ingredient)

def get_ingredient_by_code(db: Session, code: str):
    """Busca un ingrediente por su código."""
    ingredient = ingredient_repository.get_ingredient_by_code(db, code)
    if ingredient :
        return {
             "id": ingredient.id,
            "name": ingredient.name,
            "code": ingredient.code,
            "available_units": ingredient.available_units,
            "max_capacity": ingredient.max_capacity,
            "type": ingredient.type,
        }
    return None