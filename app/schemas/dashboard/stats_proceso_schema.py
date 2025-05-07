# app/schemas/dashboard/stats_proceso_schema.py

from pydantic import BaseModel
from typing import List, Optional
from app.schemas.dashboard.stats_personal_schema import CountItem, MonthCountItem, MonthTopItem

class EstadisticasProcesoResponse(BaseModel):
    """
    Respuesta para /reportes/proceso con filtrado por año:
     - candidatos_por_mes: total de candidatos registrados cada mes del año
     - top_estados_anual: conteo por estado en todo el año
     - top_estados_por_mes: estado más frecuente por mes
    """
    candidatos_por_mes: List[MonthCountItem]
    top_estados_anual: List[CountItem]
    top_estados_por_mes: List[MonthTopItem]

    class Config:
        from_attributes = True
