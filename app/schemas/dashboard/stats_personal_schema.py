# schemas/dashboard/stats_personal_schema.py

from pydantic import BaseModel
from typing import List, Optional

class CountItem(BaseModel):
    """
    Modelo genérico para un elemento con etiqueta y su conteo.
    Ejemplo: {'label': 'Bogotá', 'count': 42}
    """
    label: str
    count: int

class BooleanStats(BaseModel):
    """
    Estadísticas simples basadas en campos booleanos del modelo Candidato.
    """
    referidos: int
    no_referidos: int
    formularios_completos: int
    formularios_incompletos: int
    trabaja_actualmente_joyco: int
    ha_trabajado_joyco: int

class MonthCountItem(BaseModel):
    """
    Conteo de candidatos por mes en un año específico.
    month: número de mes (1 = enero, ..., 12 = diciembre)
    count: cantidad de candidatos registrados en ese mes.
    """
    month: int
    count: int

class MonthTopItem(BaseModel):
    """
    Top de un ítem (ciudad o cargo) en un mes concreto.
    month: número de mes
    label: nombre del ítem (ciudad o cargo)
    count: cantidad registrada en ese mes
    """
    month: int
    label: str
    count: int

class EstadisticasPersonalesResponse(BaseModel):
    """
    Respuesta extendida para /reportes/personal con filtrado por año:
     - candidatos_por_mes: total de candidatos registrados cada mes
     - top_ciudades_anual: top 5 ciudades en todo el año
     - top_ciudades_por_mes: ciudad más frecuente por cada mes
     - rangos_edad: distribución de edad (todo el año)
     - estado_candidatos: conteo de estados (todo el año)
     - estadisticas_booleanas: campos booleanos (todo el año)
     - top_cargos_anual: top 5 cargos en todo el año
     - top_cargos_por_mes: cargo más frecuente por cada mes
    """
    candidatos_por_mes: List[MonthCountItem]
    top_ciudades_anual: List[CountItem]
    top_ciudades_por_mes: List[MonthTopItem]
    rangos_edad: List[CountItem]
    estado_candidatos: List[CountItem]
    estadisticas_booleanas: BooleanStats
    top_cargos_anual: List[CountItem]
    top_cargos_por_mes: List[MonthTopItem]
    top_nombres_referidos: List[CountItem]

