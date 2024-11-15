from sqlalchemy.orm import Session
from app.persistance.models.product_model import Product
from app.domain.schemas.product_schema import ProductCreate

def create_product(db: Session, product: ProductCreate):
    db_product = Product(code=product.code, name=product.name, unit_price=product.unit_price)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db: Session):
    return db.query(Product).all()

def get_product_by_code(db: Session, code: str):
    return db.query(Product).filter(Product.code == code).first()

def update_product(db: Session, id_product: int, new_product: ProductCreate):
    product = db.query(Product).filter(Product.id_product == id_product).first()
    if not product:
        return None
    product.code = new_product.code
    product.name = new_product.name
    product.unit_price = new_product.unit_price
    db.commit()
    db.refresh(product)
    return product

def delete_product(db: Session, id_product: int):
    product = db.query(Product).filter(Product.id_product == id_product).first()
    if not product:
        return False
    db.delete(product)
    db.commit()
    return True
