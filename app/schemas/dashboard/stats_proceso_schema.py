"""Esquema de respuesta para estadísticas del proceso de selección en el dashboard."""

from pydantic import BaseModel
from typing import List
from app.schemas.dashboard.stats_personal_schema import CountItem, MonthCountItem, MonthTopItem


class EstadisticasProcesoResponse(BaseModel):
    """
    Esquema de respuesta para `/reportes/proceso`.

    Contiene:
    - candidatos_por_mes: cantidad de candidatos registrados por mes
    - top_estados_anual: distribución de estados del proceso durante el año
    - top_estados_por_mes: estado más frecuente por mes
    """
    candidatos_por_mes: List[MonthCountItem]
    top_estados_anual: List[CountItem]
    top_estados_por_mes: List[MonthTopItem]

    class Config:
        from_attributes = True  # Compatible con objetos ORM
