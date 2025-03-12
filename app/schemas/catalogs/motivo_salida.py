from typing import Optional
from pydantic import BaseModel

# Schema para representar un motivo de salida
class MotivoSalidaResponse(BaseModel):
    id_motivo_salida: int
    descripcion_motivo: str

    class Config:
        from_attributes = True

# Schema para crear un motivo de salida
class MotivoSalidaCreate(BaseModel):
    descripcion_motivo: str

# Schema para actualizar un motivo de salida
class MotivoSalidaUpdate(BaseModel):
    descripcion_motivo: Optional[str] = None
