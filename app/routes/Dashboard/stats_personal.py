"""Ruta para obtener estadísticas de información personal de los candidatos."""

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
    Retorna estadísticas relacionadas con la información personal de los candidatos.

    Estadísticas devueltas:
    - candidatos_por_mes: total de registros mensuales en el año indicado.
    - top_ciudades_anual: top 5 ciudades con más registros en el año.
    - top_ciudades_por_mes: ciudad más frecuente por mes.
    - rangos_edad: distribución de edades (por rangos) durante el año.
    - estado_candidatos: cantidad de candidatos por estado ('EN_PROCESO', 'DESCARTADO', etc.).
    - estadisticas_booleanas: conteo de respuestas booleanas (trabaja en Joyco, ha trabajado, tiene referido, etc.).
    - top_cargos_anual: top 5 cargos solicitados en el año.
    - top_cargos_por_mes: cargo más frecuente por mes.

    Args:
        año (Optional[int]): Año a filtrar. Si no se indica, agrupa todos los años.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        EstadisticasPersonalesResponse: Diccionario con estadísticas personales consolidadas.
    """
    return obtener_estadisticas_personales(db, año)
