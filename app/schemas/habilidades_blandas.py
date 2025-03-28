"""from pydantic import BaseModel
from typing import List

# Schema para representar una habilidad blanda
class HabilidadBlandaResponse(BaseModel):
    id_habilidad_blanda: int
    nombre_habilidad: str

    class Config:
        from_attributes = True

# Schema para crear una nueva habilidad blanda
class HabilidadBlandaCreate(BaseModel):
    nombre_habilidad: str

# Schema para actualizar una habilidad blanda existente
class HabilidadBlandaUpdate(BaseModel):
    nombre_habilidad: str

# Schema para asignar múltiples habilidades blandas a un candidato
class HabilidadBlandaCandidatoCreate(BaseModel):
    id_candidato: int
    id_habilidades_blandas: List[int]  # Lista de IDs de habilidades blandas

# Schema para devolver todas las habilidades blandas de un candidato
class HabilidadBlandaCandidatoListResponse(BaseModel):
    id_candidato: int
    habilidades_blandas: List[HabilidadBlandaResponse]  # Lista de habilidades blandas

    class Config:
        from_attributes = True
"""