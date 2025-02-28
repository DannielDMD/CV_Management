from typing import Optional
from pydantic import BaseModel

# Schema para representar la disponibilidad
class DisponibilidadResponse(BaseModel):
    id_disponibilidad: int
    descripcion_disponibilidad: str

    class Config:
        from_attributes = True

# Schema para representar el rango salarial
class RangoSalarialResponse(BaseModel):
    id_rango_salarial: int
    descripcion_rango: str

    class Config:
        from_attributes = True

# Schema para representar los motivos de salida
class MotivoSalidaResponse(BaseModel):
    id_motivo_salida: Optional[int]
    descripcion_motivo: Optional[str]

    class Config:
        from_attributes = True

# Schema para crear preferencias y disponibilidad
class PreferenciaDisponibilidadCreate(BaseModel):
    id_candidato: int
    disponibilidad_viajar: bool
    id_disponibilidad_inicio: int
    id_rango_salarial: int
    trabaja_actualmente: bool
    id_motivo_salida: Optional[int] = None
    razon_trabajar_joyco: Optional[str] = None

# Schema para actualizar preferencias y disponibilidad (todos los campos opcionales)
class PreferenciaDisponibilidadUpdate(BaseModel):
    disponibilidad_viajar: Optional[bool] = None
    id_disponibilidad_inicio: Optional[int] = None
    id_rango_salarial: Optional[int] = None
    trabaja_actualmente: Optional[bool] = None
    id_motivo_salida: Optional[int] = None
    razon_trabajar_joyco: Optional[str] = None

# Schema para devolver información de preferencias y disponibilidad
class PreferenciaDisponibilidadResponse(BaseModel):
    id_preferencia: int
    disponibilidad_viajar: bool
    disponibilidad: DisponibilidadResponse
    rango_salarial: RangoSalarialResponse
    trabaja_actualmente: bool
    motivo_salida: Optional[MotivoSalidaResponse]
    razon_trabajar_joyco: Optional[str]

    class Config:
        from_attributes = True
