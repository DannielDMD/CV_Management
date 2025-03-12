from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel
#Imports de los catalogos
from app.schemas.catalogs.ciudad import *
from app.schemas.catalogs.cargo_ofrecido import *
from app.schemas.catalogs.categoria_cargo import *
from app.schemas.catalogs.motivo_salida import *

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
