# routes/Dashboard/stats_personal.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.dashboard.stats_personal_service import obtener_estadisticas_personales
from app.schemas.dashboard.stats_personal_schema import EstadisticasPersonalesResponse

router = APIRouter(
    prefix="/reportes/personal",
    tags=["Reportes – Info Personal"]
)

@router.get(
    "/",
    response_model=EstadisticasPersonalesResponse,
    summary="Obtener estadísticas de información personal de los candidatos"
)
def estadisticas_personales(db: Session = Depends(get_db)):
    """
    Devuelve un objeto con:
    - Top 5 ciudades de residencia de los candidatos.
    - Distribución por rangos de edad.
    - Conteo por estado de cada candidato.
    - Estadísticas de campos booleanos (referidos, formularios completos, Joyco).
    """
    return obtener_estadisticas_personales(db)
