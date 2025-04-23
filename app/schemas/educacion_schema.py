from datetime import date
from typing import Optional
from pydantic import BaseModel, field_validator
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

    @field_validator("anio_graduacion")
    @classmethod
    def validar_anio_graduacion(cls, value: Optional[int]) -> Optional[int]:
        if value is None:
            return value  # permitido ser nulo

        año_actual = date.today().year

        if value < 1930:
            raise ValueError("El año de graduación no puede ser menor a 1930.")
        if value > año_actual:
            raise ValueError(f"El año de graduación no puede ser mayor a {año_actual}.")
        if len(str(value)) != 4:
            raise ValueError("El año de graduación debe tener 4 dígitos.")
        return value

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
