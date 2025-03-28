from typing import Optional
from pydantic import BaseModel
from app.schemas.catalogs.nivel_educacion import *
from app.schemas.catalogs.titulo import *
from app.schemas.catalogs.instituciones import *
from app.schemas.catalogs.nivel_ingles import *
# Schema para crear una educación
class EducacionCreate(BaseModel):
    id_candidato: int
    id_nivel_educacion: int
    id_titulo: Optional[int] = None
    id_institucion: Optional[int] = None
    anio_graduacion: Optional[int] = None
    id_nivel_ingles: int

# Schema para actualizar una educación (todos los campos opcionales)
class EducacionUpdate(BaseModel):
    id_nivel_educacion: Optional[int] = None
    id_titulo: Optional[int] = None
    id_institucion: Optional[int] = None
    anio_graduacion: Optional[int] = None
    id_nivel_ingles: Optional[int] = None

# Schema para devolver información de una educación
class EducacionResponse(BaseModel):
    id_educacion: int
    nivel_educacion: NivelEducacionResponse
    titulo: Optional[TituloObtenidoResponse] = None
    institucion: Optional[InstitucionAcademicaResponse] = None
    anio_graduacion: Optional[int] = None
    nivel_ingles: NivelInglesResponse

    class Config:
        from_attributes = True
