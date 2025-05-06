# routes/Dashboard/stats_proceso.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.candidato_service import obtener_estadisticas_candidatos
from app.schemas.dashboard.stats_proceso_schema import EstadisticasCandidatosResponse

router = APIRouter(
    prefix="/reportes/proceso",
    tags=["Reportes – Proceso"]
)

@router.get(
    "/",
    response_model=EstadisticasCandidatosResponse,
    summary="Obtener estadísticas del estado de los candidatos"
)
def estadisticas_proceso(db: Session = Depends(get_db)):
    """
    Devuelve:
    - Total de candidatos
    - Cantidad por estado (EN_PROCESO, ADMITIDO, ENTREVISTA, etc.)
    """
    return obtener_estadisticas_candidatos(db)
