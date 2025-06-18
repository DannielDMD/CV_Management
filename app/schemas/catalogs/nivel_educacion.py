"""Esquemas Pydantic para la entidad Nivel de Educación."""

from typing import List
from pydantic import BaseModel, Field


class NivelEducacionCreate(BaseModel):
    """
    Esquema para crear un nuevo nivel de educación.

    Atributos:
        descripcion_nivel (str): Descripción del nivel educativo.
    """
    descripcion_nivel: str = Field(..., min_length=2, max_length=100)


class NivelEducacionUpdate(BaseModel):
    """
    Esquema para actualizar un nivel de educación.

    Atributos:
        descripcion_nivel (Optional[str]): Nueva descripción del nivel.
    """
    descripcion_nivel: str | None = Field(None, min_length=2, max_length=100)


class NivelEducacionResponse(BaseModel):
    """
    Esquema de respuesta con información de un nivel educativo.

    Atributos:
        id_nivel_educacion (int): ID único del nivel educativo.
        descripcion_nivel (str): Descripción del nivel educativo.
    """
    id_nivel_educacion: int
    descripcion_nivel: str

    class Config:
        from_attributes = True  # Permite uso con modelos ORM

class NivelEducacionPaginatedResponse(BaseModel):
    total: int
    page: int
    per_page: int
    total_pages: int
    resultados: List[NivelEducacionResponse]