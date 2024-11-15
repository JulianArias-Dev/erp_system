from sqlalchemy.orm import Session
from app.persistance.repository import product_repository
from app.domain.schemas.product_schema import ProductCreate

def create_product(db: Session, product: ProductCreate):
    return product_repository.create_product(db, product)

def list_products(db: Session):
    return product_repository.get_products(db)

def update_product(db: Session, id_product: int, new_product: ProductCreate):
    return product_repository.update_product(db, id_product, new_product)

def delete_product(db: Session, id_product: int):
    return product_repository.delete_product(db, id_product)

def get_product_by_code(db: Session, code: str):
    return product_repository.get_product_by_code(db, code)
