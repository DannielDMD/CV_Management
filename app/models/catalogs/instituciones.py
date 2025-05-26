"""Modelo de la tabla 'instituciones_academicas'."""

from sqlalchemy import Column, Integer, String
from app.core.database import Base

class InstitucionAcademica(Base):
    """
    Representa una institución académica registrada.

    Atributos:
        id_institucion (int): Identificador único de la institución.
        nombre_institucion (str): Nombre de la institución académica.
    """
    __tablename__ = "instituciones_academicas"
    
    id_institucion = Column(Integer, primary_key=True, index=True)
    nombre_institucion = Column(String(150), nullable=False, unique=True)
