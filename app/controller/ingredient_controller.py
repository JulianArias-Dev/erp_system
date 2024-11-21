from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config import get_db
from app.domain.schemas.ingredient_schema import IngredientCreate, IngredientResponse
from app.domain.services import ingredient_service

router = APIRouter(prefix="/ingredients", tags=["Ingredients"])

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_ingredient(ingredient: IngredientCreate, db: Session = Depends(get_db)):
    """
    Endpoint para crear un nuevo ingrediente.
    """
    return ingredient_service.create_ingredient(db, ingredient)

@router.get("/", response_model=list[IngredientResponse])
def list_ingredients(db: Session = Depends(get_db)):
    """
    Endpoint para obtener todos los ingredientes.
    """
    return ingredient_service.list_ingredients(db)

@router.get("/{code}", response_model=IngredientResponse)
def get_ingredient_by_code(code: str, db: Session = Depends(get_db)):
    """
    Endpoint para obtener un ingrediente por su código.
    """
    ingredient = ingredient_service.get_ingredient_by_code(db, code)
    if not ingredient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="ingredient not found"
        )
    return ingredient

@router.put("/{id_ingredient}", response_model=dict)
def update_ingredient(id_ingredient: int, new_ingredient: IngredientCreate, db: Session = Depends(get_db)):
    """
    Endpoint para actualizar un ingrediente existente.
    """
    ingredient = ingredient_service.update_ingredient(db, id_ingredient, new_ingredient)
    if not ingredient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Error updating ingredient: ingredient not found"
        )
    return ingredient

@router.delete("/{id_ingredient}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ingredient(id_ingredient: int, db: Session = Depends(get_db)):
    """
    Endpoint para eliminar un ingrediente por su ID.
    """
    if not ingredient_service.delete_ingredient(db, id_ingredient):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Error deleting ingredient: ingredient not found"
        )