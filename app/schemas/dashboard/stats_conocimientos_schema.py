# schemas/dashboard/stats_conocimientos_schema.py

from pydantic import BaseModel
from typing import List, Optional
from app.schemas.dashboard.stats_personal_schema import CountItem, MonthCountItem, MonthTopItem

class EstadisticasConocimientosResponse(BaseModel):
    """
    Respuesta para /reportes/conocimientos con filtrado por año:
     - conocimientos_por_mes: total de registros de conocimientos cada mes del año
     - top_habilidades_blandas_anual: Top 5 habilidades blandas en todo el año
     - top_habilidades_blandas_por_mes: habilidad blanda más frecuente por mes
     - top_habilidades_tecnicas_anual: Top 5 habilidades técnicas en todo el año
     - top_habilidades_tecnicas_por_mes: habilidad técnica más frecuente por mes
     - top_herramientas_anual: Top 5 herramientas en todo el año
     - top_herramientas_por_mes: herramienta más frecuente por mes
    """
    conocimientos_por_mes: List[MonthCountItem]
    top_habilidades_blandas_anual: List[CountItem]
    top_habilidades_blandas_por_mes: List[MonthTopItem]
    top_habilidades_tecnicas_anual: List[CountItem]
    top_habilidades_tecnicas_por_mes: List[MonthTopItem]
    top_herramientas_anual: List[CountItem]
    top_herramientas_por_mes: List[MonthTopItem]
