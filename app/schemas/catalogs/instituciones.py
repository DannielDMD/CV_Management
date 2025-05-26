"""Esquemas Pydantic para la entidad Institución Académica."""

from pydantic import BaseModel


class InstitucionAcademicaBase(BaseModel):
    """
    Base para creación y respuesta de instituciones académicas.

    Atributos:
        nombre_institucion (str): Nombre de la institución educativa.
    """
    nombre_institucion: str


class InstitucionAcademicaCreate(InstitucionAcademicaBase):
    """Esquema para crear una nueva institución académica."""
    pass


class InstitucionAcademicaUpdate(BaseModel):
    """
    Esquema para actualizar una institución académica.

    Atributos:
        nombre_institucion (Optional[str]): Nuevo nombre de la institución.
    """
    nombre_institucion: str | None = None


class InstitucionAcademicaResponse(InstitucionAcademicaBase):
    """
    Esquema de respuesta con el identificador de la institución.

    Atributos:
        id_institucion (int): ID único de la institución académica.
    """
    id_institucion: int

    class Config:
        from_attributes = True  # Permite conversión desde modelos ORM
