from sqlalchemy.orm import Session
from app.persistance.repository import ingredient_repository
from app.domain.schemas.ingredient_schema import IngredientCreate

def create_ingredient(db: Session, ingredient: IngredientCreate):
    """Crea un nuevo ingrediente."""
    return ingredient_repository.create_ingrediet(db, ingredient)

def list_ingredients(db: Session):
    """Devuelve una lista de todos los ingredientes."""
    return ingredient_repository.get_ingredients(db)

def update_ingredient(db: Session, id_ingredient: int, new_ingredient: IngredientCreate):
    """Actualiza un ingrediente existente."""
    return ingredient_repository.update_ingredient(db, id_ingredient, new_ingredient)

def delete_ingredient(db: Session, id_ingredient: int):
    """Elimina un ingrediente por su ID."""
    return ingredient_repository.delete_ingredient(db, id_ingredient)

def get_ingredient_by_code(db: Session, code: str):
    """Busca un ingrediente por su código."""
    return ingredient_repository.get_ingredient_by_code(db, code)