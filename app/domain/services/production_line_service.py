from app.persistance.repository import production_line_repository

def get_production_lines_with_workers(db):
    """
    Servicio para recuperar líneas de producción con sus empleados asociados.
    """
    return production_line_repository.get_all_production_lines_with_workers(db)
