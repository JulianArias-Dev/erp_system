from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from app.config import get_db
from app.domain.services import recipe_service
from app.domain.schemas.recipe_schema import RecipeResponse, RecipeCreate

router = APIRouter(prefix="/recipes", tags=["Recipes"])

@router.get("/", response_model=dict, status_code=status.HTTP_200_OK)
def get_recipes(db: Session = Depends(get_db)):
    """
    Endpoint para obtener todas las recetas.
    """
    return recipe_service.get_recipes_with_ingredients(db)

@router.post("/", response_model=RecipeResponse, status_code=status.HTTP_201_CREATED)
def create_recipe(recipe: RecipeCreate, db: Session = Depends(get_db)):
    """
    Endpoint para crear una receta nueva.
    """
    return recipe_service.create_recipe(db, recipe)

@router.get("/{recipe_id}", response_model=RecipeResponse, status_code=status.HTTP_200_OK)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    """
    Endpoint para buscar una receta por su ID.
    """
    return recipe_service.get_recipe_by_id(db, recipe_id)

@router.put("/{recipe_id}", response_model=RecipeResponse, status_code=status.HTTP_200_OK)
def update_recipe(recipe_id: int, recipe: RecipeCreate, db: Session = Depends(get_db)):
    """
    Endpoint para actualizar una receta.
    """
    return recipe_service.update_recipe(db, recipe_id, recipe)


@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    """
    Endpoint para eliminar una receta.
    """
    recipe_service.delete_recipe(db, recipe_id)
    return