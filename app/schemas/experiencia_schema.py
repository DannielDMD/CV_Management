from typing import Optional
from datetime import date
from pydantic import BaseModel
from app.schemas.catalogs.rango_experiencia import *


# Schema para crear una experiencia laboral
class ExperienciaLaboralCreate(BaseModel):
    id_candidato: int
    id_rango_experiencia: int
    ultima_empresa: str
    ultimo_cargo: str
    funciones: Optional[str] = None
    fecha_inicio: date
    fecha_fin: Optional[date] = None

# Schema para actualizar una experiencia laboral (todos los campos opcionales)
class ExperienciaLaboralUpdate(BaseModel):
    id_rango_experiencia: Optional[int] = None
    ultima_empresa: Optional[str] = None
    ultimo_cargo: Optional[str] = None
    funciones: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None

# Schema para devolver información de una experiencia laboral
class ExperienciaLaboralResponse(BaseModel):
    id_experiencia: int
    rango_experiencia: RangoExperienciaResponse
    ultima_empresa: str
    ultimo_cargo: str
    funciones: Optional[str]
    fecha_inicio: date
    fecha_fin: Optional[date]

    class Config:
        from_attributes = True