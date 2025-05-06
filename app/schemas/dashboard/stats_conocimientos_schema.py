# schemas/dashboard/stats_conocimientos_schema.py

from pydantic import BaseModel
from typing import List
from app.schemas.dashboard.stats_personal_schema import CountItem

class EstadisticasConocimientosResponse(BaseModel):
    """
    Respuesta para /reportes/conocimientos:
     - top_habilidades_blandas: Top 5 de habilidades blandas más comunes
     - top_habilidades_tecnicas: Top 5 de habilidades técnicas más comunes
     - top_herramientas: Top 5 de herramientas más comunes
    """
    top_habilidades_blandas: List[CountItem]
    top_habilidades_tecnicas: List[CountItem]
    top_herramientas: List[CountItem]
