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

def group_orders_by_product(db: Session):
    """
    Agrupa las órdenes por producto y organiza las fechas con sus cantidades.
    Si una fecha ya existe, se suma la cantidad en lugar de agregar una nueva entrada.
    Las órdenes de cada producto se devuelven ordenadas por fecha.
    """
    orders = order_repository.get_orders(db)
    grouped_products = {}

    for order in orders:
        # Inicializar el diccionario del producto si no existe
        if order.product_id not in grouped_products:
            grouped_products[order.product_id] = {
                "id": order.product_id,
                "nombre": order.product.name,
                "orders": []
            }
        
        # Buscar si ya existe una orden con la misma fecha
        existing_order = next(
            (o for o in grouped_products[order.product_id]["orders"] if o["date"] == str(order.date)),
            None
        )

        if existing_order:
            # Si ya existe, sumamos la cantidad
            existing_order["quantity"] += order.quantity
        else:
            # Si no existe, agregamos una nueva entrada
            grouped_products[order.product_id]["orders"].append({
                "quantity": order.quantity,
                "date": str(order.date)  # Convertir fecha a string para evitar problemas de serialización
            })

    # Ordenar las órdenes por fecha para cada producto
    for product in grouped_products.values():
        product["orders"].sort(key=lambda o: o["date"])

    return list(grouped_products.values())

