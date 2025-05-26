"""Esquemas Pydantic para la entidad Ciudad."""

from pydantic import BaseModel


class CiudadBase(BaseModel):
    """
    Base común para creación y respuesta de ciudades.

    Atributos:
        nombre_ciudad (str): Nombre de la ciudad.
    """
    nombre_ciudad: str


class CiudadCreate(CiudadBase):
    """
    Esquema para crear una nueva ciudad.
    """
    pass


class CiudadResponse(CiudadBase):
    """
    Esquema de respuesta al consultar una ciudad.

    Atributos:
        id_ciudad (int): Identificador único de la ciudad.
    """
    id_ciudad: int

    class Config:
        from_attributes = True  # Permite compatibilidad con objetos ORM
