from pydantic import BaseModel

# Schema para representar las habilidades blandas
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

# Schema para asignar una habilidad blanda a un candidato
class HabilidadBlandaCandidatoCreate(BaseModel):
    id_candidato: int
    id_habilidad_blanda: int

# Schema para devolver la relación entre candidato y habilidades blandas
class HabilidadBlandaCandidatoResponse(BaseModel):
    id: int
    habilidad_blanda: HabilidadBlandaResponse

    class Config:
        from_attributes = True
