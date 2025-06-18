"""Esquemas Pydantic para la entidad Motivo de Salida."""

from typing import List, Optional
from pydantic import BaseModel


class MotivoSalidaResponse(BaseModel):
    """
    Esquema de respuesta para un motivo de salida registrado.

    Atributos:
        id_motivo_salida (int): ID único del motivo.
        descripcion_motivo (str): Descripción del motivo de salida.
    """
    id_motivo_salida: int
    descripcion_motivo: str

    class Config:
        from_attributes = True  # Habilita compatibilidad con modelos ORM


class MotivoSalidaCreate(BaseModel):
    """
    Esquema para crear un nuevo motivo de salida.

    Atributos:
        descripcion_motivo (str): Descripción del motivo de salida.
    """
    descripcion_motivo: str


class MotivoSalidaUpdate(BaseModel):
    """
    Esquema para actualizar parcialmente un motivo de salida.

    Atributos:
        descripcion_motivo (Optional[str]): Nueva descripción, si se proporciona.
    """
    descripcion_motivo: Optional[str] = None
    
class MotivoSalidaPaginatedResponse(BaseModel):
    total: int
    page: int
    per_page: int
    total_pages: int
    resultados: List[MotivoSalidaResponse]