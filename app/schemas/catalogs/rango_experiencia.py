"""Esquemas Pydantic para la entidad Rango de Experiencia."""

from pydantic import BaseModel
from typing import Optional


class RangoExperienciaBase(BaseModel):
    """
    Base común para creación y respuesta de rangos de experiencia.

    Atributos:
        descripcion_rango (str): Descripción del rango de experiencia.
    """
    descripcion_rango: str


class RangoExperienciaCreate(RangoExperienciaBase):
    """Esquema para crear un nuevo rango de experiencia."""
    pass


class RangoExperienciaUpdate(BaseModel):
    """
    Esquema para actualizar un rango de experiencia existente.

    Atributos:
        descripcion_rango (Optional[str]): Nueva descripción del rango, si aplica.
    """
    descripcion_rango: Optional[str] = None


class RangoExperienciaResponse(RangoExperienciaBase):
    """
    Esquema de respuesta para un rango de experiencia registrado.

    Atributos:
        id_rango_experiencia (int): ID único del rango.
    """
    id_rango_experiencia: int

    class Config:
        from_attributes = True  # Permite compatibilidad con modelos ORM
