# schemas/dashboard/stats_experiencia_schema.py

from pydantic import BaseModel
from typing import List
from app.schemas.dashboard.stats_personal_schema import CountItem

class EstadisticasExperienciaResponse(BaseModel):
    """
    Respuesta para /reportes/experiencia:
     - top_rangos_experiencia: Top de rangos de experiencia (texto)
     - top_ultimos_cargos: Top 5 de últimos cargos más frecuentes
     - top_ultimas_empresas: Top 5 de últimas empresas más frecuentes
     - distribucion_duracion: Distribución de duración de la experiencia en categorías
    """
    top_rangos_experiencia: List[CountItem]
    top_ultimos_cargos: List[CountItem]
    top_ultimas_empresas: List[CountItem]
    distribucion_duracion: List[CountItem]
