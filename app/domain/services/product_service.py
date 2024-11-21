from sqlalchemy.orm import Session
from app.persistance.repository import product_repository
from app.domain.schemas.product_schema import ProductCreate

def create_product(db: Session, product: ProductCreate):
    """Crea un nuevo producto."""
    return product_repository.create_product(db, product)

def list_products(db: Session):
    """Devuelve una lista de todos los productos."""
    return product_repository.get_products(db)

def update_product(db: Session, id_product: int, new_product: ProductCreate):
    """Actualiza un producto existente."""
    return product_repository.update_product(db, id_product, new_product)

def delete_product(db: Session, id_product: int):
    """Elimina un producto por su ID."""
    return product_repository.delete_product(db, id_product)

def get_product_by_code(db: Session, code: str):
    """Busca un producto por su código."""
    return product_repository.get_product_by_code(db, code)
