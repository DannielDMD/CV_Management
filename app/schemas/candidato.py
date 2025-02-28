from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel

# Schema para representar los catálogos relacionados con Candidato
class CiudadResponse(BaseModel):
    id_ciudad: int
    nombre_ciudad: str

    class Config:
        from_attributes = True

class CategoriaCargoResponse(BaseModel):
    id_categoria: int
    nombre_categoria: str

    class Config:
        from_attributes = True

class CargoOfrecidoResponse(BaseModel):
    id_cargo: int
    nombre_cargo: str

    class Config:
        from_attributes = True

class MotivoSalidaResponse(BaseModel):
    id_motivo_salida: Optional[int]
    nombre_motivo: Optional[str]

    class Config:
        from_attributes = True

# Schema para crear un candidato
class CandidatoCreate(BaseModel):
    nombre_completo: str
    correo_electronico: str
    cc: str
    fecha_nacimiento: Optional[date] = None
    telefono: str
    id_ciudad: int
    descripcion_perfil: Optional[str] = None
    id_categoria_cargo: int
    id_cargo: int
    trabaja_actualmente_joyco: bool
    ha_trabajado_joyco: bool
    id_motivo_salida: Optional[int] = None
    tiene_referido: bool
    nombre_referido: Optional[str] = None

# Schema para actualizar un candidato (todos los campos opcionales)
class CandidatoUpdate(BaseModel):
    nombre_completo: Optional[str] = None
    correo_electronico: Optional[str] = None
    cc: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    telefono: Optional[str] = None
    id_ciudad: Optional[int] = None
    descripcion_perfil: Optional[str] = None
    id_categoria_cargo: Optional[int] = None
    id_cargo: Optional[int] = None
    trabaja_actualmente_joyco: Optional[bool] = None
    ha_trabajado_joyco: Optional[bool] = None
    id_motivo_salida: Optional[int] = None
    tiene_referido: Optional[bool] = None
    nombre_referido: Optional[str] = None

# Schema para devolver información de un candidato
class CandidatoResponse(BaseModel):
    id_candidato: int
    nombre_completo: str
    correo_electronico: str
    cc: str
    fecha_nacimiento: Optional[date]
    telefono: str
    ciudad: CiudadResponse
    descripcion_perfil: Optional[str]
    categoria_cargo: CategoriaCargoResponse
    cargo: CargoOfrecidoResponse
    motivo_salida: Optional[MotivoSalidaResponse]
    trabaja_actualmente_joyco: bool
    ha_trabajado_joyco: bool
    tiene_referido: bool
    nombre_referido: Optional[str]
    fecha_registro: datetime

    class Config:
        from_attributes = True
