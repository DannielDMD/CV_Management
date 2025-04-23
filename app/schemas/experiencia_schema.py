import re
from typing import Optional
from datetime import date
from pydantic import BaseModel, field_validator, model_validator
from app.schemas.catalogs.rango_experiencia import *


class ExperienciaLaboralCreate(BaseModel):
    id_candidato: int
    id_rango_experiencia: int
    ultima_empresa: str
    ultimo_cargo: str
    funciones: Optional[str] = None
    fecha_inicio: date
    fecha_fin: Optional[date] = None

    @field_validator("ultima_empresa")
    @classmethod
    def validar_empresa(cls, value: str) -> str:
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9\s.,\-()]+$", value):
            raise ValueError("El nombre de la empresa contiene caracteres inválidos.")
        return value

    @field_validator("ultimo_cargo")
    @classmethod
    def validar_cargo(cls, value: str) -> str:
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9\s.,\-()]+$", value):
            raise ValueError("El cargo contiene caracteres inválidos.")
        return value

    @field_validator("funciones")
    @classmethod
    def validar_funciones(cls, value: Optional[str]) -> Optional[str]:
        if value and not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9\s.,\-():;!?¡¿\"]+$", value):
            raise ValueError("Las funciones contienen caracteres no válidos.")
        return value

    @model_validator(mode="before")
    @classmethod
    def validar_fechas(cls, values):
        fecha_inicio = values.get("fecha_inicio")
        fecha_fin = values.get("fecha_fin")
        hoy = date.today()

        if fecha_inicio > hoy:
            raise ValueError("La fecha de inicio no puede ser futura.")
        if fecha_inicio.year < 1970:
            raise ValueError("La fecha de inicio no puede ser anterior a 1970.")

        if fecha_fin:
            if fecha_fin > hoy:
                raise ValueError("La fecha de finalización no puede ser futura.")
            if fecha_fin < fecha_inicio:
                raise ValueError("La fecha de finalización no puede ser anterior a la fecha de inicio.")

        return values

# Schema para actualizar una experiencia laboral (todos los campos opcionales)
class ExperienciaLaboralUpdate(BaseModel):
    id_rango_experiencia: Optional[int] = None
    ultima_empresa: Optional[str] = None
    ultimo_cargo: Optional[str] = None
    funciones: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None

# Schema para devolver información de una experiencia laboral
class ExperienciaLaboralResponse(BaseModel):
    id_experiencia: int
    rango_experiencia: RangoExperienciaResponse
    ultima_empresa: str
    ultimo_cargo: str
    funciones: Optional[str]
    fecha_inicio: date
    fecha_fin: Optional[date]

    class Config:
        from_attributes = True