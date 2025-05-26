"""Esquema de respuesta para estadísticas de preferencias y disponibilidad en el dashboard."""

from pydantic import BaseModel
from typing import List
from app.schemas.dashboard.stats_personal_schema import CountItem, MonthCountItem, MonthTopItem


class EstadisticasPreferenciasResponse(BaseModel):
    """
    Esquema de respuesta para `/reportes/preferencias`.

    Incluye estadísticas anuales y mensuales relacionadas con:
    - preferencias registradas por mes
    - disponibilidad de inicio laboral
    - rangos salariales
    - motivos de salida
    - disposición para viajar
    - situación laboral actual
    """
    preferencias_por_mes: List[MonthCountItem]
    top_disponibilidad_inicio_anual: List[CountItem]
    top_disponibilidad_inicio_por_mes: List[MonthTopItem]
    top_rangos_salariales_anual: List[CountItem]
    top_rangos_salariales_por_mes: List[MonthTopItem]
    top_motivos_salida_anual: List[CountItem]
    top_motivos_salida_por_mes: List[MonthTopItem]
    disponibilidad_viajar_anual: List[CountItem]
    disponibilidad_viajar_por_mes: List[MonthTopItem]
    situacion_laboral_actual_anual: List[CountItem]
    situacion_laboral_actual_por_mes: List[MonthTopItem]
