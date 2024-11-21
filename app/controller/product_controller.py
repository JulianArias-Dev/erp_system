from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config import get_db
from app.domain.schemas.product_schema import ProductCreate, ProductResponse
from app.domain.services import product_service

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """
    Endpoint para crear un nuevo producto.
    """
    return product_service.create_product(db, product)

@router.get("/", response_model=list[ProductResponse])
def list_products(db: Session = Depends(get_db)):
    """
    Endpoint para obtener todos los productos.
    """
    return product_service.list_products(db)

@router.get("/{code}", response_model=ProductResponse)
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
    return product

@router.put("/{id_product}", response_model=ProductResponse)
def update_product(id_product: int, new_product: ProductCreate, db: Session = Depends(get_db)):
    """
    Endpoint para actualizar un producto existente.
    """
    product = product_service.update_product(db, id_product, new_product)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Error updating product: Product not found"
        )
    return product

@router.delete("/{id_product}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id_product: int, db: Session = Depends(get_db)):
    """
    Endpoint para eliminar un producto por su ID.
    """
    if not product_service.delete_product(db, id_product):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Error deleting product: Product not found"
        )
