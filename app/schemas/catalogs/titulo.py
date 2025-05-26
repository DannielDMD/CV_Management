"""Esquemas Pydantic para la entidad Título Obtenido."""

from pydantic import BaseModel


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
