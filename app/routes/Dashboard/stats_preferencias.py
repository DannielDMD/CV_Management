# routes/Dashboard/stats_preferencias.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.dashboard.stats_preferencias_service import obtener_estadisticas_preferencias
from app.schemas.dashboard.stats_preferencias_schema import EstadisticasPreferenciasResponse

router = APIRouter(
    prefix="/reportes/preferencias",
    tags=["Reportes – Preferencias"]
)

@router.get(
    "/",
    response_model=EstadisticasPreferenciasResponse,
    summary="Obtener estadísticas de preferencias y disponibilidad de los candidatos"
)
def estadisticas_preferencias(db: Session = Depends(get_db)):
    """
    Devuelve:
    - Distribución por inicio de disponibilidad
    - Distribución por rangos salariales
    - Distribución por motivos de salida
    - Conteo de disponibilidad para viajar (Sí/No)
    - Conteo de situación laboral actual (Sí/No)
    """
    return obtener_estadisticas_preferencias(db)
