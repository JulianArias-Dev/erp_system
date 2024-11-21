from sqlalchemy.orm import Session
from app.persistance.models.supplier_model import Supplier
from app.persistance.models.ingredient_model import Ingredient
from app.domain.schemas.supplier_schema import SupplierCreate, SupplierUpdate, SupplierIngredientAdd
from app.persistance.models.supplier_ingredient_model import SupplierIngredient


def get_all_suppliers_with_ingredients(db: Session):
    """
    Recupera todos los proveedores con sus ingredientes asociados.
    """
    suppliers = db.query(Supplier).all()
    result = []
    for supplier in suppliers:
        ingredients = [
            {
                "ingredient_id": si.ingredient.id,
                "ingredient_name": si.ingredient.name,
                "quantity": si.quantity,
                "price": si.price,
            }
            for si in supplier.ingredients
        ]
        result.append({
            "id": supplier.id,
            "name": supplier.name,
            "contact": supplier.contact,
            "ingredients": ingredients,
        })
    return result

def get_supplier_by_id(db: Session, supplier_id: int):
    """
    Obtiene un proveedor por ID, incluyendo sus ingredientes.
    """
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()

    if not supplier:
        return None

    # Construir la lista de ingredientes
    ingredients = [
        {
            "ingredient_id": si.ingredient.id,
            "ingredient_name": si.ingredient.name,
            "quantity": si.quantity,
            "price": si.price,
        }
        for si in supplier.ingredients  # Relación con SupplierIngredient
    ]

    # Retornar el proveedor con los ingredientes formateados
    return {
        "id": supplier.id,
        "name": supplier.name,
        "contact": supplier.contact,
        "ingredients": ingredients,
    }

def create_supplier(db: Session, supplier: SupplierCreate):
    """
    Crea un nuevo proveedor.
    """
    new_supplier = Supplier(name=supplier.name, contact=supplier.contact)
    db.add(new_supplier)
    db.commit()
    db.refresh(new_supplier)
    return new_supplier

def update_supplier(db: Session, supplier_id: int, supplier: SupplierUpdate):
    """
    Actualiza un proveedor existente.
    """
    existing_supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not existing_supplier:
        return None

    existing_supplier.name = supplier.name
    existing_supplier.contact = supplier.contact
    db.commit()
    db.refresh(existing_supplier)
    return existing_supplier

def delete_supplier(db: Session, supplier_id: int):
    """
    Elimina un proveedor existente.
    """
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if supplier:
        db.delete(supplier)
        db.commit()

def add_ingredient_to_supplier(db: Session, supplier_id: int, ingredient: SupplierIngredientAdd):
    """
    Agrega un ingrediente a un proveedor.
    """
    # Verifica si el proveedor existe
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        raise ValueError("Supplier not found")

    # Verifica si el ingrediente existe
    ingredient_db = db.query(Ingredient).filter(Ingredient.id == ingredient.ingredient_id).first()
    if not ingredient_db:
        raise ValueError("Ingredient not found")

    # Verifica si ya existe la relación
    existing = (
        db.query(SupplierIngredient)
        .filter(SupplierIngredient.fk_supplier == supplier_id, SupplierIngredient.fk_ingredient == ingredient.ingredient_id)
        .first()
    )
    if existing:
        raise ValueError("Ingredient already associated with supplier")

    # Crear la relación
    supplier_ingredient = SupplierIngredient(
        fk_supplier=supplier_id,
        fk_ingredient=ingredient.ingredient_id,
        quantity=ingredient.quantity,
        price=ingredient.price,
    )
    db.add(supplier_ingredient)
    db.commit()
    db.refresh(supplier_ingredient)

    return {
        "ingredient_id": supplier_ingredient.fk_ingredient,
        "ingredient_name": ingredient_db.name,
        "quantity": supplier_ingredient.quantity,
        "price": supplier_ingredient.price,
    }

def remove_ingredient_from_supplier(db: Session, supplier_id: int, ingredient_id: int):
    """
    Elimina un ingrediente asociado a un proveedor.
    """
    # Verifica si la relación existe
    supplier_ingredient = (
        db.query(SupplierIngredient)
        .filter(SupplierIngredient.fk_supplier == supplier_id, SupplierIngredient.fk_ingredient == ingredient_id)
        .first()
    )
    if not supplier_ingredient:
        raise ValueError("Ingredient not associated with supplier")

    # Eliminar la relación
    db.delete(supplier_ingredient)
    db.commit()

def validateRelationShip(db:Session, supplier_id: int, ingredient_id: int):
    supplier_ingredient = (
        db.query(SupplierIngredient)
        .filter(SupplierIngredient.fk_supplier == supplier_id, SupplierIngredient.fk_ingredient == ingredient_id)
        .first()
    )
    if not supplier_ingredient:
        raise ValueError("Ingredient not associated with supplier")
    return True

def get_supplier_toName(db: Session, supplier_id: int): 
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier :
        raise ValueError("Supplier don't exist")
    return supplier