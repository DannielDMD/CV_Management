"""Esquema de respuesta para estadísticas de experiencia laboral en el dashboard."""

from pydantic import BaseModel
from typing import List
from app.schemas.dashboard.stats_personal_schema import CountItem, MonthCountItem, MonthTopItem


class EstadisticasExperienciaResponse(BaseModel):
    """
    Esquema de respuesta para `/reportes/experiencia`.

    Contiene estadísticas anuales y mensuales sobre:
    - registros de experiencia laboral por mes
    - rangos de experiencia más frecuentes
    - últimos cargos ocupados
    - últimas empresas trabajadas
    - distribución de duración de experiencia
    """
    experiencias_por_mes: List[MonthCountItem]
    top_rangos_experiencia_anual: List[CountItem]
    top_rangos_por_mes: List[MonthTopItem]
    top_ultimos_cargos_anual: List[CountItem]
    top_ultimos_cargos_por_mes: List[MonthTopItem]
    top_ultimas_empresas_anual: List[CountItem]
    top_ultimas_empresas_por_mes: List[MonthTopItem]
    distribucion_duracion: List[CountItem]
