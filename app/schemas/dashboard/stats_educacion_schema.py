"""Esquema de respuesta para estadísticas de educación en el dashboard."""

from pydantic import BaseModel
from typing import List
from app.schemas.dashboard.stats_personal_schema import CountItem, MonthCountItem, MonthTopItem


class EstadisticasEducacionResponse(BaseModel):
    """
    Esquema de respuesta para `/reportes/educacion`.

    Incluye estadísticas educativas generales y mensuales:
    - educaciones_por_mes: cantidad de registros por mes
    - top_niveles_educacion_anual: niveles de educación más frecuentes en el año
    - top_niveles_por_mes: nivel educativo más frecuente por mes
    - top_titulos_obtenidos_anual: títulos más frecuentes en el año
    - top_titulos_por_mes: título más frecuente por mes
    - top_instituciones_academicas_anual: instituciones más mencionadas en el año
    - top_instituciones_por_mes: institución más frecuente por mes
    - distribucion_nivel_ingles_anual: frecuencia de niveles de inglés en el año
    - distribucion_nivel_ingles_por_mes: nivel de inglés más común por mes
    - distribucion_anio_graduacion: distribución por año de graduación (sin filtro por mes)
    """
    educaciones_por_mes: List[MonthCountItem]
    top_niveles_educacion_anual: List[CountItem]
    top_niveles_por_mes: List[MonthTopItem]
    top_titulos_obtenidos_anual: List[CountItem]
    top_titulos_por_mes: List[MonthTopItem]
    top_instituciones_academicas_anual: List[CountItem]
    top_instituciones_por_mes: List[MonthTopItem]
    distribucion_nivel_ingles_anual: List[CountItem]
    distribucion_nivel_ingles_por_mes: List[MonthTopItem]
    distribucion_anio_graduacion: List[CountItem]
