"""Esquemas Pydantic para estadísticas de información personal en el dashboard."""

from pydantic import BaseModel
from typing import List


class CountItem(BaseModel):
    """
    Elemento con etiqueta y su conteo.

    Ejemplo:
        {
            "label": "Bogotá",
            "count": 42
        }
    """
    label: str
    count: int


class BooleanStats(BaseModel):
    """
    Estadísticas agrupadas por campos booleanos del modelo Candidato.
    """
    referidos: int
    no_referidos: int
    formularios_completos: int
    formularios_incompletos: int
    trabaja_actualmente_joyco: int
    ha_trabajado_joyco: int


class MonthCountItem(BaseModel):
    """
    Conteo total por mes.

    Atributos:
        month (int): Número del mes (1-12).
        count (int): Cantidad de registros.
    """
    month: int
    count: int


class MonthTopItem(BaseModel):
    """
    Ítem más frecuente en un mes específico.

    Atributos:
        month (int): Número del mes (1-12).
        label (str): Nombre del ítem.
        count (int): Cantidad de registros del ítem.
    """
    month: int
    label: str
    count: int


class EstadisticasPersonalesResponse(BaseModel):
    """
    Esquema de respuesta para `/reportes/personal`.

    Incluye:
    - Conteo mensual de candidatos
    - Top de ciudades y cargos
    - Rangos de edad
    - Estado de los candidatos
    - Estadísticas de campos booleanos
    - Top de nombres de referidos
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
