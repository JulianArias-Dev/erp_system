from sqlalchemy.orm import Session
from sqlalchemy import update
from app.persistance.models.date_entry_model import DateEntry
from datetime import timedelta
import random

def get_date_by_name(db: Session, name: str):
    """Consulta la fecha por el nombre."""
    return db.query(DateEntry).filter(DateEntry.name == name).first() 

def update_date_by_name(db: Session, name: str):
    """Actualiza la fecha incrementando 6 horas y un número aleatorio de minutos."""
    # Obtener la entrada actual
    entry = db.query(DateEntry).filter(DateEntry.name == name).first()
    if not entry:
        raise ValueError(f"No se encontró una entrada con el nombre '{name}'.")

    # Incrementar 6 horas y minutos aleatorios
    new_date = entry.date + timedelta(hours=random.randint(0, 24), minutes=random.randint(1, 60))

    # Actualizar la entrada en la base de datos
    db.execute(
        update(DateEntry)
        .where(DateEntry.name == name)
        .values(date=new_date)
    )
    db.commit()
    return new_date
