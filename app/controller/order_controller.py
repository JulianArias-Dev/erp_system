from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from app.config import get_db
from app.domain.services import order_service
from app.domain.schemas.order_schema import OrderRegister
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.get("/", response_model=dict, status_code=status.HTTP_200_OK)
def get_orders(db:Session = Depends(get_db)):
    """
    Endpoint para obtener las Ordenes 
    """
    return order_service.list_orders(db)

@router.put("/saveOrder", response_model=dict)
def send_out_product(order: OrderRegister, db: Session = Depends(get_db)):
    """
    Endpoint para simular el registro de pedidos.
    """
    try:
        order = order_service.save_order(order, db)
        
        # Convertir la fecha a string para evitar problemas de serialización
        order["date"] = str(order["date"])
        
        return JSONResponse(
            content={"message": "Order successfully registered", "order": order},
            status_code=status.HTTP_201_CREATED,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


@router.get("/grouped-order-by-products", response_model=list[dict])
def get_grouped_products_with_orders(db: Session = Depends(get_db)):
    """
    Endpoint para obtener productos agrupados con fechas y cantidades.
    """
    try:
        grouped_products = order_service.group_orders_by_product(db)
        return grouped_products
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while grouping products"
        ) 

