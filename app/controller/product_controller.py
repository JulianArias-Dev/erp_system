from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.config import get_db
from app.domain.schemas.product_schema import ProductCreate
from app.domain.services import product_service

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """
    Endpoint para crear un nuevo producto.
    """
    created_product = product_service.create_product(db, product)
    return JSONResponse(
        content={"message": "Product created successfully", "product": created_product},
        status_code=status.HTTP_201_CREATED
    )

@router.get("/", response_model=dict)
def list_products(db: Session = Depends(get_db)):
    """
    Endpoint para obtener todos los productos en formato JSON.
    """
    products = product_service.list_products(db)
    return JSONResponse(content={"products": products})

@router.get("/{code}", response_model=dict)
def get_product_by_code(code: str, db: Session = Depends(get_db)):
    """
    Endpoint para obtener un producto por su código.
    """
    product = product_service.get_product_by_code(db, code)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return JSONResponse(content={"product": product})

@router.put("/{id_product}", response_model=dict)
def update_product(id_product: int, new_product: ProductCreate, db: Session = Depends(get_db)):
    """
    Endpoint para actualizar un producto existente.
    """
    updated_product = product_service.update_product(db, id_product, new_product)
    if not updated_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Error updating product: Product not found"
        )
    return JSONResponse(
        content={"message": "Product updated successfully", "product": updated_product}
    )

@router.delete("/{id_product}", response_model=dict, status_code=status.HTTP_200_OK)
def delete_product(id_product: int, db: Session = Depends(get_db)):
    """
    Endpoint para eliminar un producto por su ID.
    """
    success = product_service.delete_product(db, id_product)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Error deleting product: Product not found"
        )
    return JSONResponse(content={"message": "Product deleted successfully"})

@router.post("/production", response_model=dict, status_code=status.HTTP_202_ACCEPTED)
def production_request_endpoint(product_id: int, quantity: int, db: Session = Depends(get_db)):
    """
    Endpoint para solicitar producción.
    Llama al servicio que procesa la producción y maneja posibles errores.
    """
    try:
        # Llamada al servicio de producción
        result = product_service.production_request(product_id, quantity, db)
        return result
    except HTTPException as e:
        # Re-lanza excepciones HTTP si fueron levantadas en el servicio
        raise e
    """ except Exception as e:
        # Manejo genérico para errores inesperados
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno en el servidor. Por favor, intente más tarde."
        ) """
    
    