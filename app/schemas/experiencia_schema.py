"""Esquemas Pydantic para la gestión de experiencia laboral de los candidatos."""

import re
from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, field_validator, model_validator

from app.schemas.catalogs.rango_experiencia import RangoExperienciaResponse


class ExperienciaLaboralCreate(BaseModel):
    """
    Esquema para crear un nuevo registro de experiencia laboral asociado a un candidato.
    """
    id_candidato: int
    id_rango_experiencia: int
    ultima_empresa: str
    ultimo_cargo: str
    funciones: Optional[str] = None
    fecha_inicio: date
    fecha_fin: Optional[date] = None

    # Validación de caracteres permitidos en el nombre de la empresa
    @field_validator("ultima_empresa")
    @classmethod
    def validar_empresa(cls, value: str) -> str:
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9\s.,\-()]+$", value):
            raise ValueError("El nombre de la empresa contiene caracteres inválidos.")
        return value

    # Validación de caracteres permitidos en el nombre del cargo
    @field_validator("ultimo_cargo")
    @classmethod
    def validar_cargo(cls, value: str) -> str:
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9\s.,\-()]+$", value):
            raise ValueError("El cargo contiene caracteres inválidos.")
        return value

    # Validación opcional para el campo de funciones
    @field_validator("funciones")
    @classmethod
    def validar_funciones(cls, value: Optional[str]) -> Optional[str]:
        if value and not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9\s.,\-():;!?¡¿\"]+$", value):
            raise ValueError("Las funciones contienen caracteres no válidos.")
        return value

    # Validaciones de fechas lógicas
    @model_validator(mode="before")
    @classmethod
    def validar_fechas(cls, values):
        fecha_inicio = values.get("fecha_inicio")
        fecha_fin = values.get("fecha_fin")
        hoy = date.today()

        # Conversión de string a date si es necesario
        if isinstance(fecha_inicio, str):
            fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
        if fecha_fin and isinstance(fecha_fin, str):
            fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()

        if fecha_inicio > hoy:
            raise ValueError("La fecha de inicio no puede ser futura.")
        if fecha_inicio.year < 1970:
            raise ValueError("La fecha de inicio no puede ser anterior a 1970.")
        if fecha_fin:
            if fecha_fin > hoy:
                raise ValueError("La fecha de finalización no puede ser futura.")
            if fecha_fin < fecha_inicio:
                raise ValueError("La fecha de finalización no puede ser anterior a la de inicio.")
        return values


class ExperienciaLaboralUpdate(BaseModel):
    """
    Esquema para actualizar un registro de experiencia laboral.
    Todos los campos son opcionales.
    """
    id_rango_experiencia: Optional[int] = None
    ultima_empresa: Optional[str] = None
    ultimo_cargo: Optional[str] = None
    funciones: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None


class ExperienciaLaboralResponse(BaseModel):
    """
    Esquema de respuesta para un registro de experiencia laboral.
    """
    id_experiencia: int
    rango_experiencia: RangoExperienciaResponse
    ultima_empresa: str
    ultimo_cargo: str
    funciones: Optional[str]
    fecha_inicio: date
    fecha_fin: Optional[date]

    class Config:
        from_attributes = True
