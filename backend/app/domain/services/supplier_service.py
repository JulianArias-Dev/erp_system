from app.persistance.repository import supplier_repository
from app.domain.schemas.supplier_schema import SupplierCreate, SupplierIngredientAdd, SupplierUpdate

def get_suppliers_with_ingredients(db):
    """
    Servicio para recuperar proveedores con ingredientes.
    """
    return supplier_repository.get_all_suppliers_with_ingredients(db)

def get_supplier_by_id(db, supplier_id: int):
    """
    Servicio para obtener un proveedor por ID.
    """
    return supplier_repository.get_supplier_by_id(db, supplier_id)


def create_supplier(db, supplier: SupplierCreate):
    """
    Servicio para crear un nuevo proveedor.
    """
    return supplier_repository.create_supplier(db, supplier)

def update_supplier(db, supplier_id: int, supplier: SupplierUpdate):
    """
    Servicio para actualizar un proveedor.
    """
    return supplier_repository.update_supplier(db, supplier_id, supplier)

def delete_supplier(db, supplier_id: int):
    """
    Servicio para eliminar un proveedor.
    """
    supplier_repository.delete_supplier(db, supplier_id)

def add_ingredient_to_supplier(db, supplier_id: int, ingredient: SupplierIngredientAdd):
    """
    Servicio para agregar un ingrediente a un proveedor.
    """
    return supplier_repository.add_ingredient_to_supplier(db, supplier_id, ingredient)


def remove_ingredient_from_supplier(db, supplier_id: int, ingredient_id: int):
    """
    Servicio para eliminar un ingrediente de un proveedor.
    """
    supplier_repository.remove_ingredient_from_supplier(db, supplier_id, ingredient_id)
