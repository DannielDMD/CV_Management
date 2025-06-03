"""Modelo de la tabla 'centros_costos'."""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class CentroCostos(Base):
    """
    Representa un centro de costos de la empresa.

    Atributos:
        id_centro_costos (int): Identificador único del centro de costos.
        nombre_centro_costos (str): Nombre del centro de costos.
        candidatos (List[Candidato]): Candidatos que pertenecen a este centro.
    """
    __tablename__ = "centros_costos"

    id_centro_costos = Column(Integer, primary_key=True, index=True)
    nombre_centro_costos = Column(String(150), nullable=False, unique=True)

    # Relación inversa con candidatos
    candidatos = relationship("Candidato", back_populates="centro_costos")
