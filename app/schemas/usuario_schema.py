"""Esquemas Pydantic para la gestión de usuarios del sistema."""

from pydantic import BaseModel, EmailStr
from typing import Optional


# ──────────────── ESQUEMA BASE ────────────────

class UsuarioBase(BaseModel):
    """
    Esquema base para los datos del usuario.

    Atributos:
        correo (EmailStr): Correo electrónico del usuario.
        nombre (Optional[str]): Nombre del usuario.
        rol (str): Rol asignado ('TH' o 'ADMIN').
    """
    correo: EmailStr
    nombre: Optional[str] = None
    rol: str


# ──────────────── CREACIÓN ────────────────

class UsuarioCreate(UsuarioBase):
    """
    Esquema para crear un nuevo usuario.
    Hereda de UsuarioBase.
    """
    pass


# ──────────────── RESPUESTA ────────────────

class UsuarioOut(UsuarioBase):
    """
    Esquema de salida para retornar la información de un usuario.

    Atributos:
        id (int): ID único del usuario.
        activo (bool): Estado de activación del usuario.
    """
    id: int
    activo: bool

    class Config:
        orm_mode = True  # Compatibilidad con modelos ORM
