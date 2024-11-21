from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config import get_db
from app.domain.services import supplier_service
from app.domain.schemas.supplier_schema import SupplierCreate, SupplierIngredientAdd, SupplierUpdate, SupplierResponse, SupplierIngredientResponse

router = APIRouter(prefix="/suppliers", tags=["Suppliers"])

@router.get("/", response_model=list[SupplierResponse])
def list_suppliers(db: Session = Depends(get_db)):
    """
    Endpoint para listar todos los proveedores junto con sus ingredientes asociados.
    """
    return supplier_service.get_suppliers_with_ingredients(db)

@router.get("/{supplier_id}", response_model=SupplierResponse)
def get_supplier(supplier_id: int, db: Session = Depends(get_db)):
    """
    Endpoint para obtener un proveedor por ID.
    """
    supplier = supplier_service.get_supplier_by_id(db, supplier_id)
    if not supplier:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found")
    return supplier

@router.post("/", response_model=SupplierResponse, status_code=status.HTTP_201_CREATED)
def create_supplier(supplier: SupplierCreate, db: Session = Depends(get_db)):
    """
    Endpoint para crear un nuevo proveedor.
    """
    return supplier_service.create_supplier(db, supplier)

@router.put("/{supplier_id}", response_model=SupplierResponse)
def update_supplier(supplier_id: int, supplier: SupplierUpdate, db: Session = Depends(get_db)):
    """
    Endpoint para actualizar un proveedor por ID.
    """
    return supplier_service.update_supplier(db, supplier_id, supplier)

@router.delete("/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_supplier(supplier_id: int, db: Session = Depends(get_db)):
    """
    Endpoint para eliminar un proveedor por ID.
    """
    supplier_service.delete_supplier(db, supplier_id)

@router.post("/{supplier_id}/ingredients", response_model=SupplierIngredientResponse)
def add_ingredient_to_supplier(
    supplier_id: int, ingredient: SupplierIngredientAdd, db: Session = Depends(get_db)
):
    """
    Endpoint para agregar un ingrediente a un proveedor.
    """
    try:
        return supplier_service.add_ingredient_to_supplier(db, supplier_id, ingredient)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{supplier_id}/ingredients/{ingredient_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_ingredient_from_supplier(
    supplier_id: int, ingredient_id: int, db: Session = Depends(get_db)
):
    """
    Endpoint para eliminar un ingrediente de un proveedor.
    """
    try:
        supplier_service.remove_ingredient_from_supplier(db, supplier_id, ingredient_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
