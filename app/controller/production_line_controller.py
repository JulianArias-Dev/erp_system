from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config import get_db
from app.domain.services import production_line_service
from app.domain.schemas.production_line_schema import ProductionLineResponse

router = APIRouter(prefix="/production_lines", tags=["Production Lines"])

@router.get("/", response_model=list[ProductionLineResponse])
def list_production_lines(db: Session = Depends(get_db)):
    """
    Endpoint para listar todas las líneas de producción junto con sus empleados asociados.
    """
    return production_line_service.get_production_lines_with_workers(db)
