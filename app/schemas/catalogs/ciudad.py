"""Esquemas Pydantic para las entidades Ciudad y Departamento."""

from pydantic import BaseModel
from typing import List, Optional


# ---------------------
# SCHEMAS DE CIUDADES
# ---------------------

class CiudadBase(BaseModel):
    """
    Base común para creación y respuesta de ciudades.
    """
    nombre_ciudad: str
    id_departamento: int  # necesario para la creación


class CiudadCreate(CiudadBase):
    """
    Esquema para crear una nueva ciudad.
    """
    pass


class CiudadShort(BaseModel):
    """
    Versión resumida para representar ciudades dentro de un departamento.
    """
    id_ciudad: int
    nombre_ciudad: str

    class Config:
        from_attributes = True


class CiudadResponse(CiudadBase):
    """
    Esquema de respuesta al consultar una ciudad, con su departamento asociado.
    """
    id_ciudad: int
    departamento: Optional["DepartamentoShort"]

    class Config:
        from_attributes = True


# ---------------------------
# SCHEMAS DE DEPARTAMENTOS
# ---------------------------

class DepartamentoBase(BaseModel):
    """
    Base común para creación y respuesta de departamentos.
    """
    nombre_departamento: str


class DepartamentoCreate(DepartamentoBase):
    """
    Esquema para crear un nuevo departamento.
    """
    pass


class DepartamentoShort(BaseModel):
    """
    Versión resumida de departamento para incluir en CiudadResponse.
    """
    id_departamento: int
    nombre_departamento: str

    class Config:
        from_attributes = True


class DepartamentoResponse(DepartamentoBase):
    """
    Esquema de respuesta al consultar un departamento, con sus ciudades asociadas.
    """
    id_departamento: int
    ciudades: List[CiudadShort] = []

    class Config:
        from_attributes = True
