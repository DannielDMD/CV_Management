# schemas/dashboard/stats_educacion_schema.py

from pydantic import BaseModel
from typing import List, Optional
from app.schemas.dashboard.stats_personal_schema import CountItem, MonthCountItem, MonthTopItem

class EstadisticasEducacionResponse(BaseModel):
    """
    Respuesta para /reportes/educacion con filtrado por año:
     - educaciones_por_mes: total de registros de educación cada mes del año
     - top_niveles_educacion_anual: Top 5 niveles de formación en todo el año
     - top_niveles_por_mes: nivel de formación más frecuente por mes
     - top_titulos_obtenidos_anual: Top 5 títulos obtenidos en todo el año
     - top_titulos_por_mes: título más frecuente por mes
     - top_instituciones_academicas_anual: Top 5 instituciones académicas en todo el año
     - top_instituciones_por_mes: institución más frecuente por mes
     - distribucion_nivel_ingles_anual: distribución por nivel de inglés en todo el año
     - distribucion_nivel_ingles_por_mes: nivel de inglés más frecuente por mes
     - distribucion_anio_graduacion: conteo por año de graduación (sin mes)
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
