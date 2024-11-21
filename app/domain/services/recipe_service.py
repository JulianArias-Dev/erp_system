from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.persistance.repository import recipe_repository
from app.domain.schemas.recipe_schema import RecipeCreate

def get_recipes_with_ingredients(db: Session):
    """
    Lógica para obtener recetas con ingredientes.
    """
    recipes = recipe_repository.get_all_recipes(db)
    result = []

    for recipe in recipes:
        # Obtener los ingredientes de cada receta
        ingredients = recipe_repository.get_ingredients_by_recipe_id(db, recipe.id)
        # Formatear ingredientes
        ingredients_list = [
            {"id": ing.id, "nombre": ing.name, "cantidad": ing.quantity}
            for ing in ingredients
        ]
        # Agregar receta al resultado
        result.append({
            "id": recipe.id,
            "preparation_time": recipe.preparation_time,
            "product": {
                "id": recipe.product.id,
                "nombre": recipe.product.name,
            } if recipe.product else None,  # Manejo de productos nulos
            "ingredients": ingredients_list
        })
    return {"recetas": result}

def create_recipe(db: Session, recipe_data: RecipeCreate):
    """
    Crea una nueva receta después de validar el producto e ingredientes.
    """
    # Validar que el producto exista
    recipe_repository.validate_product_exists(db, recipe_data.product_id)

    # Validar que los ingredientes existan
    ingredient_ids = [ingredient.id for ingredient in recipe_data.ingredients]
    recipe_repository.validate_ingredients_exist(db, ingredient_ids)

    # Crear receta
    new_recipe = recipe_repository.create_recipe(
        db,
        product_id=recipe_data.product_id,
        preparation_time=recipe_data.preparation_time,
        ingredients=[
            {"id": ingredient.id, "quantity": ingredient.quantity}
            for ingredient in recipe_data.ingredients
        ]
    )
    return new_recipe

def get_recipe_by_id(db: Session, recipe_id: int):
    """
    Busca una receta por su ID y formatea el resultado para el esquema de respuesta.
    """
    recipe = recipe_repository.get_recipe_by_id(db, recipe_id)
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La receta con id {recipe_id} no está registrada en la base de datos."
        )

    # Formatear el producto
    product = {
        "id": recipe.product.id,
        "name": recipe.product.name,
    } if recipe.product else None

    # Formatear los ingredientes
    ingredients = [
        {
            "id": ingredient.fk_ingredient,
            "name": ingredient.ingredient.name,
            "quantity": ingredient.quantity,
        }
        for ingredient in recipe.ingredients
    ]

    return {
        "id": recipe.id,
        "preparation_time": recipe.preparation_time,
        "product": product,
        "ingredients": ingredients,
    }

def update_recipe(db: Session, recipe_id: int, recipe_data: RecipeCreate):
    """
    Actualiza una receta existente después de validar el producto e ingredientes.
    """
    # Validar que el producto exista
    recipe_repository.validate_product_exists(db, recipe_data.product_id)

    # Validar que los ingredientes existan
    ingredient_ids = [ingredient.id for ingredient in recipe_data.ingredients]
    recipe_repository.validate_ingredients_exist(db, ingredient_ids)

    # Actualizar la receta
    updated_recipe = recipe_repository.update_recipe(
        db,
        recipe_id=recipe_id,
        product_id=recipe_data.product_id,
        preparation_time=recipe_data.preparation_time,
        ingredients=[
            {"id": ingredient.id, "quantity": ingredient.quantity}
            for ingredient in recipe_data.ingredients
        ]
    )

    # Formatear respuesta
    product = {
        "id": updated_recipe.product.id,
        "name": updated_recipe.product.name,
    } if updated_recipe.product else None

    ingredients = [
        {
            "id": ingredient.fk_ingredient,
            "name": ingredient.ingredient.name,
            "quantity": ingredient.quantity,
        }
        for ingredient in updated_recipe.ingredients
    ]

    return {
        "id": updated_recipe.id,
        "preparation_time": updated_recipe.preparation_time,
        "product": product,
        "ingredients": ingredients,
    }


def delete_recipe(db: Session, recipe_id: int):
    """
    Elimina una receta existente.
    """
    return recipe_repository.delete_recipe(db, recipe_id)
