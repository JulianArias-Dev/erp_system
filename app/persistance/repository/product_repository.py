from sqlalchemy.orm import Session
from app.persistance.models.product_model import Product
from app.domain.schemas.product_schema import ProductCreate

def create_product(db: Session, product: ProductCreate):
    """Crea un producto en la base de datos."""
    db_product = Product(
        code=product.code,
        name=product.name,
        unit_price=product.unit_price,
        available_units=product.available_units,
        max_capacity=product.max_capacity
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db: Session):
    """Obtiene todos los productos."""
    return db.query(Product).all()

def get_product_by_code(db: Session, code: str):
    """Obtiene un producto por su código."""
    return db.query(Product).filter(Product.code == code).first()

def update_product(db: Session, id_product: int, new_product: ProductCreate):
    """Actualiza los datos de un producto existente."""
    product = db.query(Product).filter(Product.id == id_product).first()
    if not product:
        return None
    product.code = new_product.code
    product.name = new_product.name
    product.unit_price = new_product.unit_price
    product.available_units = new_product.available_units
    product.max_capacity = new_product.max_capacity
    db.commit()
    db.refresh(product)
    return product

def delete_product(db: Session, id_product: int):
    """Elimina un producto por su ID."""
    product = db.query(Product).filter(Product.id == id_product).first()
    if not product:
        return False
    db.delete(product)
    db.commit()
    return True
