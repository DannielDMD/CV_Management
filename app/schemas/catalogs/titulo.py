"""Esquemas Pydantic para la entidad Título Obtenido."""

from typing import List
from pydantic import BaseModel

from app.schemas.catalogs.nivel_educacion import NivelEducacionResponse


class TituloObtenidoBase(BaseModel):
    """
    Base común para creación y respuesta de títulos obtenidos.

    Atributos:
        nombre_titulo (str): Nombre del título académico.
        id_nivel_educacion (int): ID del nivel de educación asociado.
    """
    nombre_titulo: str
    id_nivel_educacion: int


class TituloObtenidoCreate(TituloObtenidoBase):
    """Esquema para crear un nuevo título obtenido."""
    pass


class TituloObtenidoUpdate(BaseModel):
    """
    Esquema para actualizar un título obtenido.

    Atributos:
        nombre_titulo (Optional[str]): Nuevo nombre del título.
        id_nivel_educacion (Optional[int]): Nuevo nivel de educación asociado.
    """
    nombre_titulo: str | None = None
    id_nivel_educacion: int | None = None


class TituloObtenidoResponse(TituloObtenidoBase):
    """
    Esquema de respuesta con datos del título registrado.

    Atributos:
        id_titulo (int): ID único del título.
    """
    id_titulo: int

    class Config:
        from_attributes = True  # Permite usar modelos ORM directamente
        
        
class TituloObtenidoResponse(TituloObtenidoBase):
    id_titulo: int
    nivel_educacion: NivelEducacionResponse  # 👈 usa el que ya tienes

    class Config:
        from_attributes = True


class TituloObtenidoPaginatedResponse(BaseModel):
    total: int
    page: int
    per_page: int
    total_pages: int
    resultados: List[TituloObtenidoResponse]