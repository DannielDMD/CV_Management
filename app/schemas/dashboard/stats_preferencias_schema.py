# schemas/dashboard/stats_preferencias_schema.py

from pydantic import BaseModel
from typing import List
from app.schemas.dashboard.stats_personal_schema import CountItem

class EstadisticasPreferenciasResponse(BaseModel):
    """
    Respuesta para /reportes/preferencias:
     - disponibilidad_inicio: Distribución por tipo de inicio de disponibilidad
     - rangos_salariales: Distribución por rangos salariales
     - motivos_salida: Distribución por motivos de salida
     - disponibilidad_viajar: Conteo de disponibilidad para viajar (Sí/No)
     - situacion_laboral_actual: Conteo de candidatos que trabajan actualmente (Sí/No)
    """
    disponibilidad_inicio: List[CountItem]
    rangos_salariales: List[CountItem]
    motivos_salida: List[CountItem]
    disponibilidad_viajar: List[CountItem]
    situacion_laboral_actual: List[CountItem]
