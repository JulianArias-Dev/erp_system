from app.persistance.models.production_line_model import ProductionLine
from app.persistance.models.worker_model import Worker
from sqlalchemy.orm import joinedload

def get_all_production_lines_with_workers(db):
    """
    Recupera todas las líneas de producción junto con sus trabajadores asociados.
    """
    production_lines = (
        db.query(ProductionLine)
        .options(joinedload(ProductionLine.workers))  # Carga a los trabajadores
        .all()
    )

    result = []
    for line in production_lines:
        workers = [
            {
                "id": worker.id,
                "name": worker.name,
                "uid": worker.uid,
                "fk_production_line": worker.fk_production_line,  # Asegúrate de incluirlo
            }
            for worker in line.workers
        ]

        result.append({
            "id": line.id,
            "liquid_capacity": line.liquid_capacity,
            "solid_capacity": line.solid_capacity,
            "production_factor": line.production_factor,
            "workers": workers,
        })

    return result
