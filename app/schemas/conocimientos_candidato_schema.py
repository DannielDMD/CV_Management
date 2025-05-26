"""Esquemas Pydantic para los conocimientos asociados a un candidato."""

from pydantic import BaseModel, Field
from typing import Optional


class CandidatoConocimientoBase(BaseModel):
    """
    Esquema base para un conocimiento relacionado con un candidato.

    Atributos:
        id_candidato (int): ID del candidato asociado.
        tipo_conocimiento (str): Tipo de conocimiento ('blanda', 'tecnica' o 'herramienta').
        id_habilidad_blanda (Optional[int]): ID de la habilidad blanda (si aplica).
        id_habilidad_tecnica (Optional[int]): ID de la habilidad técnica (si aplica).
        id_herramienta (Optional[int]): ID de la herramienta (si aplica).
    """
    id_candidato: int = Field(..., title="ID del candidato")
    tipo_conocimiento: str = Field(
        ..., 
        title="Tipo de conocimiento",
        pattern="^(blanda|tecnica|herramienta)$"
    )
    id_habilidad_blanda: Optional[int] = Field(None, title="ID de la habilidad blanda")
    id_habilidad_tecnica: Optional[int] = Field(None, title="ID de la habilidad técnica")
    id_herramienta: Optional[int] = Field(None, title="ID de la herramienta")


class CandidatoConocimientoCreate(CandidatoConocimientoBase):
    """Esquema para la creación de un nuevo conocimiento del candidato."""
    pass


class CandidatoConocimientoResponse(CandidatoConocimientoBase):
    """
    Esquema de respuesta para un conocimiento registrado.

    Atributos:
        id_conocimiento (int): ID único del conocimiento.
    """
    id_conocimiento: int = Field(..., title="ID del conocimiento")

    class Config:
        from_attributes = True  # Compatible con modelos ORM
