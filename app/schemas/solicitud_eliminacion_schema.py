"""Esquemas Pydantic para la gestión de solicitudes de eliminación de datos personales por parte de los candidatos."""

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import List, Optional


# ──────────────── CREACIÓN DE SOLICITUD ────────────────

class SolicitudEliminacionCreate(BaseModel):
    """
    Esquema para recibir una nueva solicitud de eliminación desde el frontend.
    
    Atributos:
        nombre_completo (str): Nombre completo del solicitante.
        cc (str): Cédula del solicitante.
        correo (EmailStr): Correo electrónico válido.
        motivo (str): Razón de la solicitud ('Actualizar datos' o 'Eliminar candidatura').
    """
    nombre_completo: str = Field(..., max_length=255)
    cc: str = Field(..., min_length=6, max_length=20)
    correo: EmailStr
    motivo: str = Field(..., max_length=50)
    descripcion_motivo: Optional[str] = None  # Campo de texto libre


# ──────────────── RESPUESTA DE UNA SOLICITUD ────────────────

class SolicitudEliminacionResponse(BaseModel):
    """
    Esquema de respuesta para mostrar una solicitud de eliminación.
    
    Atributos:
        id (int): ID de la solicitud.
        nombre_completo (str): Nombre del solicitante.
        cc (str): Cédula del solicitante.
        correo (EmailStr): Correo electrónico.
        motivo (str): Razón de la solicitud.
        estado (str): Estado actual ('pendiente', 'atendida', 'eliminada').
        observacion_admin (Optional[str]): Observación del administrador.
        fecha_solicitud (datetime): Fecha y hora de creación de la solicitud.
    """
    id: int
    nombre_completo: str
    cc: str
    correo: EmailStr
    motivo: str
    estado: str
    descripcion_motivo: Optional[str] = None
    observacion_admin: Optional[str] = None
    fecha_solicitud: datetime

    class Config:
        from_attributes = True  # Compatible con SQLAlchemy ORM


# ──────────────── RESPUESTA PAGINADA ────────────────

class SolicitudesPaginadasResponse(BaseModel):
    """
    Respuesta paginada con solicitudes de eliminación.
    
    Atributos:
        data (List[SolicitudEliminacionResponse]): Lista de solicitudes.
        total (int): Total de solicitudes encontradas.
    """
    data: List[SolicitudEliminacionResponse]
    total: int


# ──────────────── ESTADÍSTICAS DE SOLICITUDES ────────────────

class ConteoSolicitudesEliminacion(BaseModel):
    """
    Conteo estadístico de solicitudes según su estado y motivo.
    
    Atributos:
        total (int): Total general.
        pendientes (int): Total en estado 'pendiente'.
        rechazadas (int): Total en estado 'rechazada'.
        aceptadas (int): Total en estado 'aceptada' o 'eliminada'.
        motivo_actualizar_datos (int): Total por motivo 'Actualizar datos'.
        motivo_eliminar_candidatura (int): Total por motivo 'Eliminar candidatura'.
    """
    total: int
    pendientes: int
    rechazadas: int
    aceptadas: int
    motivo_actualizar_datos: int
    motivo_eliminar_candidatura: int
