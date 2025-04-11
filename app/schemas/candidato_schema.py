from typing import Optional, List
from datetime import date, datetime
from pydantic import BaseModel

# Imports de los catalogos
from app.schemas.catalogs.ciudad import *
from app.schemas.catalogs.cargo_ofrecido import *
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
    id_cargo: Optional[int] = None
    trabaja_actualmente_joyco: Optional[bool] = None
    ha_trabajado_joyco: Optional[bool] = None
    id_motivo_salida: Optional[int] = None
    tiene_referido: Optional[bool] = None
    nombre_referido: Optional[str] = None
    estado: Optional[str] = None


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
    cargo: CargoOfrecidoResponse
    motivo_salida: Optional[MotivoSalidaResponse]
    trabaja_actualmente_joyco: bool
    ha_trabajado_joyco: bool
    tiene_referido: bool
    nombre_referido: Optional[str]
    fecha_registro: datetime
    estado: str  # ✅ nuevo campo

    class Config:
        from_attributes = True


# ───────────── SCHEMA RESUMIDO PARA DASHBOARD ─────────────


class CandidatoResumenResponse(BaseModel):
    id_candidato: int
    nombre_completo: str
    correo_electronico: str
    telefono: str
    ciudad: str
    cargo_ofrecido: str
    nivel_educativo: Optional[str] = None
    titulo_obtenido: Optional[str] = None
    rango_experiencia: Optional[str] = None
    habilidades_blandas: list[str] = []
    habilidades_tecnicas: list[str] = []
    herramientas: list[str] = []
    disponibilidad_inicio: Optional[str] = None
    trabaja_actualmente_joyco: bool
    fecha_postulacion: datetime
    estado: str
    

    class Config:
        from_attributes = True



class CandidatoResumenPaginatedResponse(BaseModel):
    data: List[CandidatoResumenResponse]
    total: int

# ───────────── SCHEMA Completo PARA DASHBOAR   D ─────────────
class CandidatoDetalleResponse(BaseModel):
    # Información Personal
    nombre_completo: str
    correo_electronico: str
    cc: str
    fecha_nacimiento: date
    telefono: str
    ciudad: str
    descripcion_perfil: Optional[str]
    cargo: str
    trabaja_actualmente_joyco: bool
    ha_trabajado_joyco: bool
    motivo_salida: Optional[str] = None
    tiene_referido: bool
    nombre_referido: Optional[str] = None
    fecha_registro: datetime
    estado: str

    # Educación
    nivel_educacion: Optional[str] = None
    titulo: Optional[str] = None
    institucion: Optional[str] = None
    anio_graduacion: Optional[int] = None
    nivel_ingles: Optional[str] = None

    # Experiencia Laboral
    rango_experiencia: Optional[str] = None
    ultima_empresa: Optional[str] = None
    ultimo_cargo: Optional[str] = None
    funciones: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None

    # Conocimientos
    habilidades_blandas: List[str]
    habilidades_tecnicas: List[str]
    herramientas: List[str]

    # Preferencias y Disponibilidad
    disponibilidad_viajar: Optional[bool] = None
    disponibilidad_inicio: Optional[str] = None
    rango_salarial: Optional[str] = None
    trabaja_actualmente: Optional[bool] = None
    motivo_salida_laboral: Optional[str] = None
    razon_trabajar_joyco: Optional[str] = None

    class Config:
        orm_mode = True
