# schemas/dashboard/stats_experiencia_schema.py

from pydantic import BaseModel
from typing import List, Optional
from app.schemas.dashboard.stats_personal_schema import CountItem, MonthCountItem, MonthTopItem

class EstadisticasExperienciaResponse(BaseModel):
    """
    Respuesta para /reportes/experiencia con filtrado por año:
     - experiencias_por_mes: total de registros de experiencia cada mes del año
     - top_rangos_experiencia_anual: Top de rangos de experiencia en todo el año
     - top_rangos_por_mes: rango de experiencia más frecuente por mes
     - top_ultimos_cargos_anual: Top 5 de últimos cargos en todo el año
     - top_ultimos_cargos_por_mes: cargo más frecuente por mes
     - top_ultimas_empresas_anual: Top 5 de empresas en todo el año
     - top_ultimas_empresas_por_mes: empresa más frecuente por mes
     - distribucion_duracion: Distribución de duración de la experiencia en categorías (todo el año)
    """
    experiencias_por_mes: List[MonthCountItem]
    top_rangos_experiencia_anual: List[CountItem]
    top_rangos_por_mes: List[MonthTopItem]
    top_ultimos_cargos_anual: List[CountItem]
    top_ultimos_cargos_por_mes: List[MonthTopItem]
    top_ultimas_empresas_anual: List[CountItem]
    top_ultimas_empresas_por_mes: List[MonthTopItem]
    distribucion_duracion: List[CountItem]
