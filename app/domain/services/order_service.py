from sqlalchemy.orm import Session
from app.persistance.repository import order_repository
from app.domain.schemas.order_schema import OrderRegister

def list_orders(db:Session):
    """Devuelve una lista de ordenes"""
    orders = order_repository.get_orders(db)
    result = []
    
    for order in orders :
        
        result.append({
            "id": order.id,
            "date": order.date,
            "product": {
                "id": order.product.id,
                "nombre": order.product.name,
            } if order.product else None,  # Manejo de productos nulos
            "quantity" : order.quantity,
        })
        
    return {"orders":result}

def save_order(order: OrderRegister, db: Session):
    """
    Simula la venta de un producto y registra el pedido.
    """
    if order.quantity <= 0:
        raise ValueError("The quantity must be greater than zero.")

    try:
        order = order_repository.send_out_product(order, db)
    except ValueError as e:
        # Propaga errores específicos de lógica
        raise ValueError(str(e))
    except Exception as e:
        # Captura errores inesperados y los registra
        print(f"Unexpected error: {e}")
        raise Exception("Failed to process the order.")

    if not order:
        raise ValueError("Error while registering the order.")

    return {
        "id": order.id,
        "date": order.date,
        "product": {
            "id": order.product.id,
            "name": order.product.name,
        } if order.product else None,  # Manejo de productos nulos
        "quantity": order.quantity,
    }
