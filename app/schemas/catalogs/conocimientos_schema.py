"""Esquemas Pydantic para habilidades blandas, técnicas y herramientas."""

from pydantic import BaseModel, Field


# ----------------------------
# Habilidad Blanda
# ----------------------------

class HabilidadBlandaBase(BaseModel):
    """
    Base para esquemas de habilidades blandas.

    Atributos:
        nombre_habilidad_blanda (str): Nombre de la habilidad blanda.
    """
    nombre_habilidad_blanda: str = Field(..., title="Nombre de la habilidad blanda", max_length=100)


class HabilidadBlandaCreate(HabilidadBlandaBase):
    """Esquema para crear una nueva habilidad blanda."""
    pass


class HabilidadBlandaResponse(HabilidadBlandaBase):
    """
    Esquema de respuesta para una habilidad blanda registrada.

    Atributos:
        id_habilidad_blanda (int): ID único de la habilidad blanda.
    """
    id_habilidad_blanda: int = Field(..., title="ID de la habilidad blanda")

    class Config:
        from_attributes = True


# ----------------------------
# Habilidad Técnica
# ----------------------------

class HabilidadTecnicaBase(BaseModel):
    """
    Base para esquemas de habilidades técnicas.

    Atributos:
        nombre_habilidad_tecnica (str): Nombre de la habilidad técnica.
    """
    nombre_habilidad_tecnica: str = Field(..., title="Nombre de la habilidad técnica", max_length=100)


class HabilidadTecnicaCreate(HabilidadTecnicaBase):
    """Esquema para crear una nueva habilidad técnica."""
    pass


class HabilidadTecnicaResponse(HabilidadTecnicaBase):
    """
    Esquema de respuesta para una habilidad técnica registrada.

    Atributos:
        id_habilidad_tecnica (int): ID único de la habilidad técnica.
    """
    id_habilidad_tecnica: int = Field(..., title="ID de la habilidad técnica")

    class Config:
        from_attributes = True


# ----------------------------
# Herramienta
# ----------------------------

class HerramientaBase(BaseModel):
    """
    Base para esquemas de herramientas.

    Atributos:
        nombre_herramienta (str): Nombre de la herramienta.
    """
    nombre_herramienta: str = Field(..., title="Nombre de la herramienta", max_length=100)


class HerramientaCreate(HerramientaBase):
    """Esquema para crear una nueva herramienta."""
    pass


class HerramientaResponse(HerramientaBase):
    """
    Esquema de respuesta para una herramienta registrada.

    Atributos:
        id_herramienta (int): ID único de la herramienta.
    """
    id_herramienta: int = Field(..., title="ID de la herramienta")

    class Config:
        from_attributes = True
