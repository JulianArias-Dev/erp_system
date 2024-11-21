from sqlalchemy.orm import Session
from app.persistance.repository import product_repository
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

def sold_product(product_code: str, sold_quantity: int, db: Session):
    """
    Simula la venta de un producto y actualiza el stock.
    """
    if sold_quantity <= 0:
        raise ValueError("Sold quantity must be greater than zero.")

    product = product_repository.send_out_product(product_code, sold_quantity, db)

    if not product:
        raise ValueError("Product not found.")
    if product.available_units < 0:
        return {
            "id": product.id,
            "code": product.code,
            "name": product.name,
            "unit_price": product.unit_price,
            "available_units": product.available_units,
            "max_capacity": product.max_capacity,
            "warning": "Inventory is negative after this sale!"
        }

    return {
        "id": product.id,
        "code": product.code,
        "name": product.name,
        "unit_price": product.unit_price,
        "available_units": product.available_units,
        "max_capacity": product.max_capacity,
    }