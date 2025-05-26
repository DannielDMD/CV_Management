"""Esquemas Pydantic para la entidad Nivel de Inglés."""

from pydantic import BaseModel


class NivelInglesResponse(BaseModel):
    """
    Esquema de respuesta para un nivel de inglés registrado.

    Atributos:
        id_nivel_ingles (int): ID único del nivel.
        nivel (str): Descripción del nivel de inglés.
    """
    id_nivel_ingles: int
    nivel: str

    class Config:
        from_attributes = True  # Compatible con modelos ORM


class NivelInglesCreate(BaseModel):
    """
    Esquema para crear un nuevo nivel de inglés.

    Atributos:
        nivel (str): Descripción del nivel.
    """
    nivel: str


class NivelInglesUpdate(BaseModel):
    """
    Esquema para actualizar un nivel de inglés existente.

    Atributos:
        nivel (str): Nueva descripción del nivel.
    """
    nivel: str
