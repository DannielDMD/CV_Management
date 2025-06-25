from pydantic import BaseModel
from typing import Dict, Optional

class EstadisticasGeneralesResponse(BaseModel):
    total_candidatos: int
    candidatos_hoy: int
    candidatos_ultima_semana: int
    edad_promedio: float
    candidatos_por_mes: Dict[int, int]
    ciudad_top: str
    cargo_top: str

    # Nuevo campo opcional para evolución por año y mes
    evolucion_anual: Optional[Dict[str, int]] = None
