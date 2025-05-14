from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import List, Optional


# 📥 Para recibir solicitudes desde el frontend
class SolicitudEliminacionCreate(BaseModel):
    nombre_completo: str = Field(..., max_length=255)
    cc: str = Field(..., min_length=6, max_length=20)
    correo: EmailStr
    motivo: str = Field(..., max_length=50)  # Ej: 'Actualizar datos', 'Eliminar candidatura'


# 📤 Para devolver solicitudes al frontend o a TH
class SolicitudEliminacionResponse(BaseModel):
    id: int
    nombre_completo: str
    cc: str
    correo: EmailStr
    motivo: str
    estado: str
    observacion_admin: Optional[str] = None
    fecha_solicitud: datetime

    class Config:
        from_attributes = True  # o orm_mode = True en FastAPI <2.0

class SolicitudesPaginadasResponse(BaseModel):
    data: List[SolicitudEliminacionResponse]
    total: int
    
class ConteoSolicitudesEliminacion(BaseModel):
    total: int
    pendientes: int
    rechazadas: int
    aceptadas: int
    motivo_actualizar_datos: int
    motivo_eliminar_candidatura: int
