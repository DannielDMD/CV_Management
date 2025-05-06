from pydantic import BaseModel
from typing import List

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
    referidos: int                  # cantidad de candidatos con tiene_referido = True
    no_referidos: int               # cantidad con tiene_referido = False
    formularios_completos: int      # formulario_completo = True
    formularios_incompletos: int    # formulario_completo = False
    trabaja_actualmente_joyco: int  # trabaja_actualmente_joyco = True
    ha_trabajado_joyco: int         # ha_trabajado_joyco = True

class EstadisticasPersonalesResponse(BaseModel):
    """
    Respuesta completa para /reportes/personal.
    """
    top_ciudades: List[CountItem]
    rangos_edad: List[CountItem]
    estado_candidatos: List[CountItem]
    estadisticas_booleanas: BooleanStats
    top_cargos: List[CountItem]  # ✅ nuevo campo agregado
