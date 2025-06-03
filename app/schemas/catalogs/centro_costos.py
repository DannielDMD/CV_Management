"""Esquemas Pydantic para la entidad CentroCostos."""

from pydantic import BaseModel


class CentroCostosBase(BaseModel):
    """
    Base común para creación y respuesta de centros de costos.

    Atributos:
        nombre_centro_costos (str): Nombre del centro de costos.
    """
    nombre_centro_costos: str


class CentroCostosCreate(CentroCostosBase):
    """
    Esquema para crear un nuevo centro de costos.
    """
    pass


class CentroCostosResponse(CentroCostosBase):
    """
    Esquema de respuesta al consultar un centro de costos.

    Atributos:
        id_centro_costos (int): Identificador único del centro.
    """
    id_centro_costos: int

    class Config:
        from_attributes = True
