"""Modelo de la tabla 'solicitudes_eliminacion'."""

from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func
from app.core.database import Base

class SolicitudEliminacion(Base):
    """
    Representa una solicitud realizada por un candidato para actualizar o eliminar su información.

    Atributos:
        id (int): Identificador único de la solicitud.
        nombre_completo (str): Nombre completo del solicitante.
        cc (str): Cédula de ciudadanía del solicitante.
        correo (str): Correo electrónico del solicitante.
        motivo (str): Motivo de la solicitud ('Actualizar datos' o 'Eliminar candidatura').
        estado (str): Estado actual de la solicitud ('pendiente', 'atendida' o 'eliminada').
        observacion_admin (str): Observación interna agregada por el administrador (opcional).
        fecha_solicitud (timestamp): Fecha en que se registró la solicitud.
    """
    __tablename__ = "solicitudes_eliminacion"

    id = Column(Integer, primary_key=True, index=True)
    nombre_completo = Column(String(255), nullable=False)
    cc = Column(String(20), nullable=False)
    correo = Column(String(150), nullable=False)
    motivo = Column(String(50), nullable=False)  # 'Actualizar datos' o 'Eliminar candidatura'
    estado = Column(String(20), nullable=False, default="pendiente")  # pendiente, atendida, eliminada
    descripcion_motivo = Column(Text, nullable=True)  # Descripción opcional del motivo
    observacion_admin = Column(Text, nullable=True)
    fecha_solicitud = Column(TIMESTAMP, server_default=func.current_timestamp())
