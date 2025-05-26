"""Esquema de respuesta para estadísticas de conocimientos en el dashboard."""

from pydantic import BaseModel
from typing import List
from app.schemas.dashboard.stats_personal_schema import CountItem, MonthCountItem, MonthTopItem


class EstadisticasConocimientosResponse(BaseModel):
    """
    Esquema de respuesta para `/reportes/conocimientos`.

    Contiene estadísticas anuales y mensuales sobre:
    - conocimientos registrados por mes
    - top habilidades blandas
    - top habilidades técnicas
    - top herramientas
    """
    conocimientos_por_mes: List[MonthCountItem]
    top_habilidades_blandas_anual: List[CountItem]
    top_habilidades_blandas_por_mes: List[MonthTopItem]
    top_habilidades_tecnicas_anual: List[CountItem]
    top_habilidades_tecnicas_por_mes: List[MonthTopItem]
    top_herramientas_anual: List[CountItem]
    top_herramientas_por_mes: List[MonthTopItem]
