from pydantic import BaseModel, Field
from typing import Optional

# Esquema base para CandidatoConocimiento
class CandidatoConocimientoBase(BaseModel):
    id_candidato: int = Field(..., title="ID del candidato")
    tipo_conocimiento: str = Field(..., title="Tipo de conocimiento", pattern="^(blanda|tecnica|herramienta)$")
    id_habilidad_blanda: Optional[int] = Field(None, title="ID de la habilidad blanda")
    id_habilidad_tecnica: Optional[int] = Field(None, title="ID de la habilidad técnica")
    id_herramienta: Optional[int] = Field(None, title="ID de la herramienta")

# Esquema para creación
class CandidatoConocimientoCreate(CandidatoConocimientoBase):
    pass

# Esquema para respuesta con ID
class CandidatoConocimientoResponse(CandidatoConocimientoBase):
    id_conocimiento: int = Field(..., title="ID del conocimiento")

    class Config:
        from_attributes = True