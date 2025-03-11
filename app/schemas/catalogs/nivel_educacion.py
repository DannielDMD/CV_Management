from pydantic import BaseModel, Field

# Schema para crear un Nivel de Educación
class NivelEducacionCreate(BaseModel):
    descripcion_nivel: str = Field(..., min_length=2, max_length=100)

# Schema para actualizar un Nivel de Educación
class NivelEducacionUpdate(BaseModel):
    descripcion_nivel: str | None = Field(None, min_length=2, max_length=100)

# Schema para responder con un Nivel de Educación
class NivelEducacionResponse(BaseModel):
    id_nivel_educacion: int
    descripcion_nivel: str

    class Config:
        from_attributes = True
