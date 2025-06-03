"""Esquemas Pydantic para gestionar la disponibilidad, rangos salariales y preferencias de los candidatos."""

from typing import Optional
from pydantic import BaseModel
from app.schemas.catalogs.motivo_salida import MotivoSalidaResponse


# ──────────────── DISPONIBILIDAD ────────────────

class DisponibilidadCreate(BaseModel):  
    """Esquema para crear una nueva disponibilidad."""
    descripcion_disponibilidad: str


class DisponibilidadUpdate(BaseModel):
    """Esquema para actualizar la descripción de una disponibilidad (opcional)."""
    descripcion_disponibilidad: Optional[str] = None


class DisponibilidadResponse(BaseModel):
    """Esquema de respuesta para una disponibilidad."""
    id_disponibilidad: int
    descripcion_disponibilidad: str

    class Config:
        from_attributes = True


# ──────────────── RANGO SALARIAL ────────────────

class RangoSalarialCreate(BaseModel):
    """Esquema para crear un nuevo rango salarial."""
    descripcion_rango: str


class RangoSalarialUpdate(BaseModel):
    """Esquema para actualizar un rango salarial (opcional)."""
    descripcion_rango: Optional[str] = None


class RangoSalarialResponse(BaseModel):
    """Esquema de respuesta para un rango salarial."""
    id_rango_salarial: int
    descripcion_rango: str

    class Config:
        from_attributes = True


# ──────────────── PREFERENCIAS Y DISPONIBILIDAD ────────────────

class PreferenciaDisponibilidadCreate(BaseModel):
    """
    Esquema para crear preferencias y disponibilidad asociadas a un candidato.
    """
    id_candidato: int
    disponibilidad_viajar: bool
    id_disponibilidad_inicio: int
    id_rango_salarial: int
    trabaja_actualmente: bool
    id_motivo_salida: Optional[int] = None
    razon_trabajar_joyco: Optional[str] = None
    otro_motivo_salida: Optional[str] = None



class PreferenciaDisponibilidadUpdate(BaseModel):
    """
    Esquema para actualizar parcialmente las preferencias y disponibilidad.
    Todos los campos son opcionales.
    """
    disponibilidad_viajar: Optional[bool] = None
    id_disponibilidad_inicio: Optional[int] = None
    id_rango_salarial: Optional[int] = None
    trabaja_actualmente: Optional[bool] = None
    id_motivo_salida: Optional[int] = None
    razon_trabajar_joyco: Optional[str] = None
    otro_motivo_salida: Optional[str] = None



class PreferenciaDisponibilidadResponse(BaseModel):
    """
    Esquema de respuesta para las preferencias y disponibilidad de un candidato.
    """
    id_preferencia: int
    disponibilidad_viajar: bool
    disponibilidad: DisponibilidadResponse
    rango_salarial: RangoSalarialResponse
    trabaja_actualmente: bool
    motivo_salida: Optional[MotivoSalidaResponse]
    razon_trabajar_joyco: Optional[str]
    otro_motivo_salida: Optional[str]


    class Config:
        from_attributes = True
