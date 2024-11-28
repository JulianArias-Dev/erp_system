from sqlalchemy.orm import Session
from app.persistance.models import Order, Product
from app.domain.schemas.order_schema import OrderRegister

def get_orders(db:Session):
    """Obtinene la lista completa de ordenes"""
    return db.query(Order).join(Product, Order.product_id==Product.id).all()

def send_out_product(order: OrderRegister, db: Session):
    """
    Actualiza el inventario y registra el pedido en la base de datos.
    """
    # try:
    product = db.query(Product).filter(Product.id == order.product_id).first()

    if not product:
        raise ValueError(f"Product with ID {order.product_id} not found.")

    # Opcional: Validar inventario positivo
    if product.available_units < order.quantity:
        print(f"Warning: Inventory going negative for product ID {order.product_id}.")

    product.available_units -= order.quantity
    db.commit()
    db.refresh(product)

    # Crear el pedido en la base de datos
    db_order = Order(
        product_id=order.product_id,
        quantity=order.quantity,
        date=order.date,
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    return db_order

    """ except Exception as e:
        db.rollback()
        print(f"Database error: {e}")
        raise Exception("Error while processing the order.") """

    