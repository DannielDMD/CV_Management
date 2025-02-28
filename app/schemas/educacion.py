from typing import Optional
from pydantic import BaseModel

# Schema para representar los catálogos relacionados con Educación
class NivelEducacionResponse(BaseModel):
    id_nivel_educacion: int
    descripcion_nivel: str

    class Config:
        from_attributes = True

class TituloObtenidoResponse(BaseModel):
    id_titulo: int
    nombre_titulo: str
    id_nivel_educacion: int

    class Config:
        from_attributes = True

class InstitucionAcademicaResponse(BaseModel):
    id_institucion: int
    nombre_institucion: str

    class Config:
        from_attributes = True

class NivelInglesResponse(BaseModel):
    id_nivel_ingles: int
    nivel: str

    class Config:
        from_attributes = True

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
