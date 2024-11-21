from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config import get_db
from app.domain.schemas.ingredient_schema import IngredientCreate, IngredientResponse
from app.domain.schemas.purchase_ingredient_schema import PurchaseIngredientCreate
from app.domain.services import ingredient_service
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/ingredients", tags=["Ingredients"])

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_ingredient(ingredient: IngredientCreate, db: Session = Depends(get_db)):
    """
    Endpoint para crear un nuevo ingrediente.
    """
    create_ingredient = ingredient_service.create_ingredient(db, ingredient)
    return JSONResponse(
        content={"message":"Ingredient created successfully", "ingredient":create_ingredient},
        status_code=status.HTTP_201_CREATED
    )

@router.get("/", response_model=dict)
def list_ingredients(db: Session = Depends(get_db)):
    """
    Endpoint para obtener todos los ingredientes en formato JSON.
    """
    ingredients = ingredient_service.list_ingredients(db)
    return JSONResponse(content={"ingredients": ingredients})


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
    return JSONResponse(content={"ingredient": ingredient})

@router.put("/{id_ingredient}", response_model=dict)
def update_ingredient(id_ingredient: int, new_ingredient: IngredientCreate, db: Session = Depends(get_db)):
    """
    Endpoint para actualizar un ingrediente existente.
    """
    updated_ingredient = ingredient_service.update_ingredient(db, id_ingredient, new_ingredient)
    if not updated_ingredient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Error updating ingredient: ingredient not found"
        )
    return JSONResponse(
        content={"message": "Ingredient updated successfully", "ingredient": updated_ingredient}
    )

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
    return JSONResponse(content={"message": "Ingredient deleted successfully"})

@router.post('/purchase', response_model=dict)
def register_purchase(purchase: PurchaseIngredientCreate, db: Session = Depends(get_db)):
    """
    Endpoint para registrar compras - Actualizar stock y enviar reporte a Finanzas.
    """
    try:
        # Llamada al servicio para registrar la compra
        data = ingredient_service.ingredient_purchase(db, purchase)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    return JSONResponse(
        {"message": "Purchase registered successfully", "data": data},
        status_code=status.HTTP_201_CREATED
    )