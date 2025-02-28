from typing import List
from pydantic import BaseModel

# Schema para representar las categorías de habilidades técnicas
class CategoriaHabilidadTecnicaResponse(BaseModel):
    id_categoria_habilidad: int
    nombre_categoria: str

    class Config:
        from_attributes = True

# Schema para representar las habilidades técnicas
class HabilidadTecnicaResponse(BaseModel):
    id_habilidad_tecnica: int
    nombre_habilidad: str
    categoria: CategoriaHabilidadTecnicaResponse

    class Config:
        from_attributes = True

# Schema para asignar una habilidad técnica a un candidato
class HabilidadTecnicaCandidatoCreate(BaseModel):
    id_candidato: int
    id_habilidad_tecnica: int

# Schema para devolver la relación entre candidato y habilidades técnicas
class HabilidadTecnicaCandidatoResponse(BaseModel):
    id: int
    habilidad_tecnica: HabilidadTecnicaResponse

    class Config:
        from_attributes = True
