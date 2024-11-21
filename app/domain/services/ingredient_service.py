import httpx
from sqlalchemy.orm import Session
from app.persistance.repository import ingredient_repository, date_entry_repository, supplier_repository
from app.domain.schemas.ingredient_schema import IngredientCreate
from app.domain.schemas.purchase_ingredient_schema import PurchaseIngredientCreate
from fastapi import HTTPException
import logging

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

def ingredient_purchase(db: Session, purchase: PurchaseIngredientCreate):
    """
    Registra la compra, actualiza la fecha y el stock, y envía un reporte al backend de finanzas.
    """
    try:
        # Validar relación entre proveedor e ingrediente
        supplier_repository.validateRelationShip(db, purchase.supplier_id, purchase.ingredient_id)
        
        # Actualizar stock del ingrediente
        ingredient = ingredient_repository.update_stock(db, purchase.ingredient_id, purchase.quantity)
        supplier = supplier_repository.get_supplier_toName(db, purchase.supplier_id)
        # Obtener y actualizar la fecha
        purchase_date = date_entry_repository.get_date_by_name(db, 'PurchaseDate')
        if not purchase_date:
            raise ValueError("No se encontró la fecha con el nombre 'PurchaseDate'")
        
        formatted_date = purchase_date.date.strftime('%Y-%m-%d')  # Formato: 'YYYY-MM-DD'
        formatted_time = purchase_date.date.strftime('%H:%M')     # Formato: 'hh:mm'
        
        # Actualizar la fecha en la base de datos
        date_entry_repository.update_date_by_name(db, 'PurchaseDate')
        
        # Preparar los datos para enviar al backend de finanzas
        finance_data = {
            "Monto": purchase.value,
            "Categoria": f"Compra de {ingredient.name}",
            "Proveedor": supplier.name,
            "Fecha": formatted_date,
            "Hora": formatted_time,
        }
        
        # Enviar solicitud POST al backend de finanzas
        response = httpx.post(
            "https://finanzasbackend-dw9a.onrender.com/api/addGastos", 
            json=finance_data,
            timeout=10
        )
        
        if response.status_code != 200:
            logging.error(f"Error al reportar a finanzas: {response.text}")
            raise HTTPException(
                status_code=500,
                detail="Error al reportar la compra al sistema de finanzas."
            )
        
        # Formatear los datos de respuesta
        return {
            "ingredient": {
                "id": ingredient.id,
                "name": ingredient.name,
                "new_stock": ingredient.available_units
            },
            "supplier_id": purchase.supplier_id,
            "quantity": purchase.quantity,
            "value": purchase.value,
            "Fecha": formatted_date,
            "Hora": formatted_time,
            "finance_response": response.json()  # Incluir respuesta del backend de finanzas
        }
    except ValueError as e:
        raise ValueError(f"Error en la compra: {str(e)}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Ocurrió un error inesperado durante el procesamiento de la compra."
        )

    

