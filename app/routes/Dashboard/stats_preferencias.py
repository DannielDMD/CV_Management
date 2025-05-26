"""Ruta para obtener estadísticas de preferencias y disponibilidad de los candidatos."""

from typing import Optional
from fastapi import APIRouter, Depends, Query
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
    summary="Obtener estadísticas de preferencias y disponibilidad de los candidatos filtradas por año"
)
def estadisticas_preferencias(
    año: Optional[int] = Query(
        None,
        title="Año",
        description="Año para filtrar las estadísticas de preferencias (por ejemplo, 2025). Si no se indica, usa todos los años."
    ),
    db: Session = Depends(get_db)
):
    """
    Retorna estadísticas sobre las preferencias laborales y disponibilidad de los candidatos.

    Estadísticas devueltas:
    - preferencias_por_mes: total de registros por mes del año indicado.
    - top_disponibilidad_inicio_anual: distribución de inicio de disponibilidad durante el año.
    - top_disponibilidad_inicio_por_mes: disponibilidad más frecuente por mes.
    - top_rangos_salariales_anual: distribución de rangos salariales en el año.
    - top_rangos_salariales_por_mes: rango salarial más frecuente por mes.
    - top_motivos_salida_anual: motivos de salida más comunes en el año.
    - top_motivos_salida_por_mes: motivo más común por mes.
    - disponibilidad_viajar_anual: conteo de candidatos dispuestos a viajar (Sí/No).
    - disponibilidad_viajar_por_mes: frecuencia de disponibilidad para viajar por mes.
    - situacion_laboral_actual_anual: conteo de situación laboral actual (trabaja o no).
    - situacion_laboral_actual_por_mes: situación más común por mes.

    Args:
        año (Optional[int]): Año a filtrar. Si no se indica, agrupa todos los años.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        EstadisticasPreferenciasResponse: Datos estadísticos consolidados de preferencias y disponibilidad.
    """
    return obtener_estadisticas_preferencias(db, año)
    