from sqlalchemy.orm import Session
from app.persistance.repository import product_repository, recipe_repository, ingredient_repository
from app.domain.schemas.product_schema import ProductCreate

def create_product(db: Session, product: ProductCreate):
    """Crea un nuevo producto y lo devuelve en formato JSON."""
    product = product_repository.create_product(db, product)
    return {
        "id": product.id,
        "code": product.code,
        "name": product.name,
        "unit_price": product.unit_price,
        "available_units": product.available_units,
        "max_capacity": product.max_capacity,
    }

def list_products(db: Session):
    """Devuelve una lista de todos los productos en formato JSON."""
    products = product_repository.get_products(db)
    return [
        {
            "id": product.id,
            "code": product.code,
            "name": product.name,
            "unit_price": product.unit_price,
            "available_units": product.available_units,
            "max_capacity": product.max_capacity,
        }
        for product in products
    ]

def get_product_by_code(db: Session, code: str):
    """Busca un producto por su código y devuelve su JSON."""
    product = product_repository.get_product_by_code(db, code)
    if product:
        return {
            "id": product.id,
            "code": product.code,
            "name": product.name,
            "unit_price": product.unit_price,
            "available_units": product.available_units,
            "max_capacity": product.max_capacity,
        }
    return None

def update_product(db: Session, id_product: int, new_product: ProductCreate):
    """Actualiza un producto existente y devuelve su JSON."""
    updated_product = product_repository.update_product(db, id_product, new_product)
    if updated_product:
        return {
            "id": updated_product.id,
            "code": updated_product.code,
            "name": updated_product.name,
            "unit_price": updated_product.unit_price,
            "available_units": updated_product.available_units,
            "max_capacity": updated_product.max_capacity,
        }
    return None

def delete_product(db: Session, id_product: int):
    """Elimina un producto por su ID."""
    return product_repository.delete_product(db, id_product)

def production_request(product_id: int, quantity: int, db: Session):
    """
    Procesa una solicitud de producción basada en el producto y su receta.
    Calcula la cantidad total requerida de cada ingrediente y verifica su disponibilidad.
    Si los ingredientes alcanzan, reduce las unidades y aumenta las unidades disponibles del producto.
    """
    # Buscar el producto por product_id
    product = product_repository.get_product_by_id(db, product_id)

    if not product:
        return {"detalle": "Producto no encontrado."}

    # Buscar la receta asociada al producto
    recipe = recipe_repository.get_recipe_by_product_id(db, product_id)

    if not recipe:
        return {"detalle": "Receta no encontrada para el producto proporcionado."}

    # Obtener los ingredientes de la receta
    ingredients = recipe_repository.get_ingredients_by_recipe_id(db, recipe.id)

    if not ingredients:
        return {"detalle": "No hay ingredientes asociados a la receta."}

    # Verificar la disponibilidad de los ingredientes
    insufficient_ingredients = []

    for ing in ingredients:
        # Consultar el estado actualizado del ingrediente en la base de datos
        current_ingredient = ingredient_repository.get_ingredient_by_code(db, ing.id)

        if not current_ingredient:
            return {"detalle": f"Ingrediente con ID {ing.id} no encontrado en la base de datos."}

        total_required = ing.quantity * quantity  # Cantidad total requerida del ingrediente

        if current_ingredient.available_units < total_required:
            insufficient_ingredients.append({
                "id": current_ingredient.id,
                "nombre": current_ingredient.name,
                "requerido": total_required,
                "disponible": current_ingredient.available_units
            })

    if insufficient_ingredients:
        return {
            "detalle": "Ingredientes insuficientes.",
            "ingredientes_faltantes": insufficient_ingredients
        }

    # Actualizar las unidades disponibles de los ingredientes
    for ing in ingredients:
        # Consultar el ingrediente nuevamente para asegurarse de usar los datos más recientes
        current_ingredient = ingredient_repository.get_ingredient_by_code(db, ing.id)

        if not current_ingredient:
            return {"detalle": f"Ingrediente con ID {ing.id} no encontrado en la base de datos."}

        total_required = ing.quantity * quantity
        current_ingredient.available_units -= total_required
        db.add(current_ingredient)  # Marcar para actualización

    # Aumentar las unidades disponibles del producto
    product.available_units += quantity
    db.add(product)  # Marcar para actualización

    # Guardar los cambios en la base de datos
    db.commit()

    return {
        "detalle": "Producción completada exitosamente.",
        "producto": {
            "id": product.id,
            "nombre": product.name,
            "unidades_disponibles": product.available_units
        }
    }