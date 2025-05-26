"""Modelo de la tabla 'ciudades'."""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class Ciudad(Base):
    """
    Representa una ciudad registrada en el sistema.

    Atributos:
        id_ciudad (int): Identificador único de la ciudad.
        nombre_ciudad (str): Nombre de la ciudad.
        candidatos (List[Candidato]): Relación con los candidatos asociados a esta ciudad.
    """
    __tablename__ = "ciudades"

    id_ciudad = Column(Integer, primary_key=True, index=True)
    nombre_ciudad = Column(String(100), nullable=False, unique=True)

    # Relación inversa con la tabla de candidatos
    candidatos = relationship("Candidato", back_populates="ciudad")
