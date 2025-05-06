# schemas/dashboard/stats_educacion_schema.py

from pydantic import BaseModel
from typing import List
from app.schemas.dashboard.stats_personal_schema import CountItem

class EstadisticasEducacionResponse(BaseModel):
    """
    Respuesta para /reportes/educacion:
     - top_niveles_educacion: Top 5 niveles de formación
     - top_titulos_obtenidos: Top 5 títulos obtenidos
     - top_instituciones_academicas: Top 5 instituciones académicas
     - distribucion_nivel_ingles: Distribución por nivel de inglés
     - distribucion_anio_graduacion: Conteo por año de graduación
    """
    top_niveles_educacion: List[CountItem]
    top_titulos_obtenidos: List[CountItem]
    top_instituciones_academicas: List[CountItem]
    distribucion_nivel_ingles: List[CountItem]
    distribucion_anio_graduacion: List[CountItem]
