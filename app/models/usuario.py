"""Modelo de la tabla 'usuarios'."""

from sqlalchemy import Column, Integer, String, Boolean
from app.core.database import Base

class Usuario(Base):
    """
    Representa un usuario registrado en el sistema (ej. personal de Talento Humano o administradores).

    Atributos:
        id (int): Identificador único del usuario.
        correo (str): Correo electrónico único del usuario.
        nombre (str): Nombre del usuario.
        rol (str): Rol del usuario ('TH' para Talento Humano, 'ADMIN' para administrador).
        activo (bool): Estado del usuario (activo o inactivo).
    """
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    correo = Column(String(255), unique=True, index=True, nullable=False)
    nombre = Column(String(255))
    rol = Column(String(20), nullable=False, default="TH")  # 'TH' o 'ADMIN'
    activo = Column(Boolean, default=True, nullable=False)
