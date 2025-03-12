from pydantic import BaseModel
from typing import Optional

# Esquema base
class RangoExperienciaBase(BaseModel):
    descripcion_rango: str

# Esquema para crear un rango de experiencia
class RangoExperienciaCreate(RangoExperienciaBase):
    pass

# Esquema para actualizar un rango de experiencia
class RangoExperienciaUpdate(BaseModel):
    descripcion_rango: Optional[str] = None

# Esquema para respuesta (lectura)
class RangoExperienciaResponse(RangoExperienciaBase):
    id_rango_experiencia: int

    class Config:
        from_attributes = True
