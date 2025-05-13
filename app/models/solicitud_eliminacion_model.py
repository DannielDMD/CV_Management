from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func
from app.core.database import Base

class SolicitudEliminacion(Base):
    __tablename__ = "solicitudes_eliminacion"

    id = Column(Integer, primary_key=True, index=True)
    nombre_completo = Column(String(255), nullable=False)
    cc = Column(String(20), nullable=False)
    correo = Column(String(150), nullable=False)
    motivo = Column(String(50), nullable=False)  # 'Actualizar datos' o 'Eliminar candidatura'
    estado = Column(String(20), nullable=False, default="pendiente")  # pendiente, atendida, eliminada
    observacion_admin = Column(Text, nullable=True)
    fecha_solicitud = Column(TIMESTAMP, server_default=func.current_timestamp())
