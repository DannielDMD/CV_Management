# routes/Dashboard/stats_personal.py

from typing import Optional
from fastapi import APIRouter, Depends, Query
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
    summary="Obtener estadísticas de información personal de los candidatos filtradas por año"
)
def estadisticas_personales(
    año: Optional[int] = Query(
        None,
        title="Año",
        description="Año para filtrar las estadísticas (por ejemplo, 2025). Si no se indica, usa todos los años."
    ),
    db: Session = Depends(get_db)
):
    """
    Devuelve un objeto con:
    - candidatos_por_mes: total de candidatos registrados cada mes del año indicado
    - top_ciudades_anual: top 5 ciudades en todo el año
    - top_ciudades_por_mes: ciudad más frecuente por mes
    - rangos_edad: distribución de edad en el año
    - estado_candidatos: conteo por estado en el año
    - estadisticas_booleanas: campos booleanos en el año
    - top_cargos_anual: top 5 cargos en el año
    - top_cargos_por_mes: cargo más frecuente por mes
    """
    return obtener_estadisticas_personales(db, año)
