"""Modelos de las tablas 'ciudades' y 'departamentos'."""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Departamento(Base):
    """
    Representa un departamento del país.

    Atributos:
        id_departamento (int): Identificador único del departamento.
        nombre_departamento (str): Nombre del departamento.
        ciudades (List[Ciudad]): Ciudades que pertenecen a este departamento.
    """
    __tablename__ = "departamentos"

    id_departamento = Column(Integer, primary_key=True, index=True)
    nombre_departamento = Column(String(100), nullable=False, unique=True)

    # Relación uno a muchos con Ciudad
    ciudades = relationship("Ciudad", back_populates="departamento")


class Ciudad(Base):
    """
    Representa una ciudad registrada en el sistema.

    Atributos:
        id_ciudad (int): Identificador único de la ciudad.
        nombre_ciudad (str): Nombre de la ciudad.
        id_departamento (int): Departamento al que pertenece la ciudad.
        departamento (Departamento): Relación con el departamento.
        candidatos (List[Candidato]): Relación con los candidatos asociados a esta ciudad.
    """
    __tablename__ = "ciudades"

    id_ciudad = Column(Integer, primary_key=True, index=True)
    nombre_ciudad = Column(String(100), nullable=False, unique=True)

    # FK hacia Departamento
    id_departamento = Column(Integer, ForeignKey("departamentos.id_departamento"), nullable=False)

    # Relación con Departamento
    departamento = relationship("Departamento", back_populates="ciudades")

    # Relación inversa con Candidato (tabla candidatos.py)
    candidatos = relationship("Candidato", back_populates="ciudad")
