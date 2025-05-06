# routes/Dashboard/stats_conocimientos.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.dashboard.stats_conocimientos_service import obtener_estadisticas_conocimientos
from app.schemas.dashboard.stats_conocimientos_schema import EstadisticasConocimientosResponse

router = APIRouter(
    prefix="/reportes/conocimientos",
    tags=["Reportes – Conocimientos"]
)

@router.get(
    "/",
    response_model=EstadisticasConocimientosResponse,
    summary="Obtener estadísticas de conocimientos de los candidatos"
)
def estadisticas_conocimientos(db: Session = Depends(get_db)):
    """
    Devuelve:
    - Top 5 habilidades blandas
    - Top 5 habilidades técnicas
    - Top 5 herramientas
    """
    return obtener_estadisticas_conocimientos(db)
