"""Modelo de la tabla 'nivel_ingles'."""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class NivelIngles(Base):
    """
    Representa los distintos niveles de inglés registrados (ej. Básico, Intermedio, Avanzado).

    Atributos:
        id_nivel_ingles (int): Identificador único del nivel de inglés.
        nivel (str): Descripción del nivel de inglés.
        educaciones (List[Educacion]): Relación con registros de educación asociados a este nivel.
    """
    __tablename__ = "nivel_ingles"

    id_nivel_ingles = Column(Integer, primary_key=True, index=True)
    nivel = Column(String(20), nullable=False, unique=True)

    # Relación con la tabla de educación
    educaciones = relationship("Educacion", back_populates="nivel_ingles")
