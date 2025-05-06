# routes/Dashboard/stats_experiencia.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.dashboard.stats_experiencia_service import obtener_estadisticas_experiencia
from app.schemas.dashboard.stats_experiencia_schema import EstadisticasExperienciaResponse

router = APIRouter(
    prefix="/reportes/experiencia",
    tags=["Reportes – Experiencia Laboral"]
)

@router.get(
    "/",
    response_model=EstadisticasExperienciaResponse,
    summary="Obtener estadísticas de experiencia laboral de los candidatos"
)
def estadisticas_experiencia(db: Session = Depends(get_db)):
    """
    Devuelve:
    - Distribución por rangos de experiencia
    - Top 5 de últimos cargos
    - Top 5 de últimas empresas
    - Distribución de duración de la experiencia en categorías
    """
    return obtener_estadisticas_experiencia(db)
