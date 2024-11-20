from sqlalchemy.orm import Session
from fastapi import HTTPException, status   
from app.persistance.models.recipe_model import Recipe
from app.persistance.models.recipe_ingredient_model import RecipeIngredients
from app.persistance.models.ingredient_model import Ingredient
from app.persistance.models.product_model import Product
from typing import List

def get_all_recipes(db: Session):
    """
    Recupera todas las recetas con sus productos.
    """
    return db.query(Recipe).join(Product, Recipe.fk_product == Product.id).all()

def get_ingredients_by_recipe_id(db: Session, recipe_id: int):
    """
    Recupera los ingredientes asociados a una receta específica.
    """
    return (
        db.query(RecipeIngredients.quantity, Ingredient.id, Ingredient.name)
        .join(Ingredient, RecipeIngredients.fk_ingredient == Ingredient.id)
        .filter(RecipeIngredients.fk_recipe == recipe_id)
        .all()
    )

def validate_product_exists(db: Session, product_id: int):
    """Valida si el producto existe en la base de datos."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El producto con id {product_id} no está registrado en la base de datos."
        )
    return product

def validate_ingredients_exist(db: Session, ingredient_ids: List[int]):
    """Valida si los ingredientes existen en la base de datos."""
    existing_ingredients = db.query(Ingredient).filter(Ingredient.id.in_(ingredient_ids)).all()
    missing_ids = set(ingredient_ids) - {ing.id for ing in existing_ingredients}

    if missing_ids:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Los siguientes ingredientes no están registrados en la base de datos: {missing_ids}"
        )
    return existing_ingredients

def create_recipe(db: Session, product_id: int, preparation_time: int, ingredients: List[dict]):
    """Crea una receta con sus ingredientes."""
    # Crear la receta
    new_recipe = Recipe(
        fk_product=product_id,
        preparation_time=preparation_time
    )
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)

    # Agregar ingredientes a la receta
    for ingredient in ingredients:
        recipe_ingredient = RecipeIngredients(
            fk_recipe=new_recipe.id,
            fk_ingredient=ingredient["id"],
            quantity=ingredient["quantity"]
        )
        db.add(recipe_ingredient)
    db.commit()

    return new_recipe

def get_recipe_by_id(db: Session, recipe_id: int):
    """Obtiene una receta por su ID."""
    return db.query(Recipe).filter(Recipe.id == recipe_id).first()

def update_recipe(db: Session, recipe_id: int, product_id: int, preparation_time: int, ingredients: List[dict]):
    """Actualiza una receta existente."""
    # Obtener la receta
    recipe = get_recipe_by_id(db, recipe_id)
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La receta con id {recipe_id} no está registrada en la base de datos."
        )

    # Actualizar campos principales de la receta
    recipe.fk_product = product_id
    recipe.preparation_time = preparation_time

    # Eliminar relaciones de ingredientes antiguas
    db.query(RecipeIngredients).filter(RecipeIngredients.fk_recipe == recipe_id).delete()

    # Agregar nuevas relaciones de ingredientes
    for ingredient in ingredients:
        new_recipe_ingredient = RecipeIngredients(
            fk_recipe=recipe_id,
            fk_ingredient=ingredient["id"],
            quantity=ingredient["quantity"]
        )
        db.add(new_recipe_ingredient)

    db.commit()
    db.refresh(recipe)
    return recipe


def delete_recipe(db: Session, recipe_id: int):
    """Elimina una receta por su ID."""
    recipe = get_recipe_by_id(db, recipe_id)
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La receta con id {recipe_id} no está registrada en la base de datos."
        )
    db.delete(recipe)
    db.commit()
    return True
