# schemas/dashboard/stats_preferencias_schema.py

from pydantic import BaseModel
from typing import List, Optional
from app.schemas.dashboard.stats_personal_schema import CountItem, MonthCountItem, MonthTopItem

class EstadisticasPreferenciasResponse(BaseModel):
    """
    Respuesta para /reportes/preferencias con filtrado por año:
     - preferencias_por_mes: total de registros de preferencias cada mes del año
     - top_disponibilidad_inicio_anual: Distribución por tipo de inicio de disponibilidad en todo el año
     - top_disponibilidad_inicio_por_mes: tipo de inicio más frecuente por mes
     - top_rangos_salariales_anual: Distribución por rangos salariales en todo el año
     - top_rangos_salariales_por_mes: rango salarial más frecuente por mes
     - top_motivos_salida_anual: Distribución por motivos de salida en todo el año
     - top_motivos_salida_por_mes: motivo de salida más frecuente por mes
     - disponibilidad_viajar_anual: Conteo de disponibilidad para viajar (Sí/No) en todo el año
     - disponibilidad_viajar_por_mes: disponibilidad para viajar más frecuente por mes
     - situacion_laboral_actual_anual: Conteo de situación laboral actual (Sí/No) en todo el año
     - situacion_laboral_actual_por_mes: situación laboral más frecuente por mes
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
