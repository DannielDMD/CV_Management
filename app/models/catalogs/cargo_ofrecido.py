"""Modelo de la tabla 'cargos_ofrecidos'."""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class CargoOfrecido(Base):
    """
    Representa los cargos ofrecidos por la organización.

    Atributos:
        id_cargo (int): Identificador único del cargo.
        nombre_cargo (str): Nombre del cargo ofrecido.
        candidatos (List[Candidato]): Relación con los candidatos que aplican a este cargo.
    """
    __tablename__ = "cargos_ofrecidos"

    id_cargo = Column(Integer, primary_key=True, index=True)
    nombre_cargo = Column(String(100), nullable=False, unique=True)

    # Relación con la tabla de candidatos
    candidatos = relationship("Candidato", back_populates="cargo")
