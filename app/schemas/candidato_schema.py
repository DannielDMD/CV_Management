import re
from typing import Optional, List
from datetime import date, datetime
from pydantic import BaseModel, EmailStr, field_validator

# Imports de los catalogos
from app.schemas.catalogs.ciudad import *
from app.schemas.catalogs.cargo_ofrecido import *
from app.schemas.catalogs.motivo_salida import *


class CandidatoCreate(BaseModel):
    nombre_completo: str
    correo_electronico: EmailStr
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

    @field_validator("fecha_nacimiento")
    @classmethod
    def validar_fecha_nacimiento(cls, value: Optional[date]) -> Optional[date]:
        if value is None:
            raise ValueError("La fecha de nacimiento es obligatoria.")
        hoy = date.today()
        edad = hoy.year - value.year - ((hoy.month, hoy.day) < (value.month, value.day))
        if value > hoy:
            raise ValueError("La fecha de nacimiento no puede ser futura.")
        if edad < 18:
            raise ValueError("Debes tener al menos 18 años.")
        if value < date(1930, 1, 1):
            raise ValueError("La fecha de nacimiento no puede ser anterior a 1930.")
        return value

    @field_validator("nombre_completo")
    @classmethod
    def validar_nombre_completo(cls, value: str) -> str:
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", value):
            raise ValueError("El nombre solo debe contener letras y espacios.")
        return value

    @field_validator("cc")
    @classmethod
    def validar_cc(cls, value: str) -> str:
        if not value.isdigit():
            raise ValueError("La cédula solo debe contener números.")
        if not (6 <= len(value) <= 10):
            raise ValueError("La cédula debe tener entre 6 y 10 dígitos.")
        return value

    @field_validator("telefono")
    @classmethod
    def validar_telefono(cls, value: str) -> str:
        if not value.isdigit():
            raise ValueError("El teléfono solo debe contener números.")
        if len(value) != 10:
            raise ValueError("El teléfono debe tener exactamente 10 dígitos.")
        return value

    @field_validator("descripcion_perfil")
    @classmethod
    def validar_descripcion_perfil(cls, value: Optional[str]) -> Optional[str]:
        if value and len(value) > 300:
            raise ValueError("La descripción del perfil no debe superar los 300 caracteres.")
        if value and not re.match(r"^[\w\s.,;:áéíóúÁÉÍÓÚñÑ()¿?¡!\"'-]*$", value):
            raise ValueError("La descripción contiene caracteres no permitidos.")
        return value

    @field_validator("nombre_referido")
    @classmethod
    def validar_nombre_referido(cls, value: Optional[str]) -> Optional[str]:
        if value and not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", value):
            raise ValueError("El nombre del referido solo debe contener letras y espacios.")
        return value

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
    formulario_completo: bool  # ✅ NUEVO CAMPO


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
        

