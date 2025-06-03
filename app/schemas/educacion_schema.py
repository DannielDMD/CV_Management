"""Esquemas Pydantic para la gestión de información educativa de los candidatos."""

from datetime import date
from typing import Optional
from pydantic import BaseModel, field_validator

# Importación de esquemas relacionados
from app.schemas.catalogs.nivel_educacion import NivelEducacionResponse
from app.schemas.catalogs.titulo import TituloObtenidoResponse
from app.schemas.catalogs.instituciones import InstitucionAcademicaResponse
from app.schemas.catalogs.nivel_ingles import NivelInglesResponse


class EducacionCreate(BaseModel):
    """
    Esquema para crear un registro de educación asociado a un candidato.

    Atributos:
        id_candidato (int): ID del candidato.
        id_nivel_educacion (int): Nivel educativo alcanzado.
        id_titulo (Optional[int]): Título obtenido.
        id_institucion (Optional[int]): Institución académica.
        anio_graduacion (Optional[int]): Año de graduación.
        id_nivel_ingles (int): Nivel de inglés.
    """
    id_candidato: int
    id_nivel_educacion: int
    id_titulo: Optional[int] = None
    id_institucion: Optional[int] = None
    nombre_titulo_otro: Optional[str] = None
    nombre_institucion_otro: Optional[str] = None
    anio_graduacion: Optional[int] = None
    id_nivel_ingles: int

    @field_validator("anio_graduacion")
    @classmethod
    def validar_anio_graduacion(cls, value: Optional[int]) -> Optional[int]:
        if value is None:
            return value  # Permitido como nulo
        año_actual = date.today().year
        if value < 1930:
            raise ValueError("El año de graduación no puede ser menor a 1930.")
        if value > año_actual:
            raise ValueError(f"El año de graduación no puede ser mayor a {año_actual}.")
        if len(str(value)) != 4:
            raise ValueError("El año de graduación debe tener 4 dígitos.")
        return value


class EducacionUpdate(BaseModel):
    """
    Esquema para actualizar un registro de educación.

    Todos los campos son opcionales.
    """
    id_nivel_educacion: Optional[int] = None
    id_titulo: Optional[int] = None
    id_institucion: Optional[int] = None
    nombre_titulo_otro: Optional[str] = None
    nombre_institucion_otro: Optional[str] = None
    anio_graduacion: Optional[int] = None
    id_nivel_ingles: Optional[int] = None


class EducacionResponse(BaseModel):
    """
    Esquema de respuesta para un registro de educación.

    Atributos:
        id_educacion (int): ID único del registro.
        nivel_educacion (NivelEducacionResponse): Nivel educativo.
        titulo (Optional): Título académico (si aplica).
        institucion (Optional): Institución educativa (si aplica).
        anio_graduacion (Optional[int]): Año de graduación.
        nivel_ingles (NivelInglesResponse): Nivel de inglés.
    """
    id_educacion: int
    nivel_educacion: NivelEducacionResponse
    titulo: Optional[TituloObtenidoResponse] = None
    institucion: Optional[InstitucionAcademicaResponse] = None
    nombre_titulo_otro: Optional[str] = None
    nombre_institucion_otro: Optional[str] = None
    anio_graduacion: Optional[int] = None
    nivel_ingles: NivelInglesResponse

    class Config:
        from_attributes = True
