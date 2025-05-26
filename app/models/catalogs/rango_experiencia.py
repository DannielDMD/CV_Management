"""Modelo de la tabla 'rangos_experiencia'."""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class RangoExperiencia(Base):
    """
    Representa los distintos rangos de experiencia laboral (ej. 0-1 años, 2-5 años, etc.).

    Atributos:
        id_rango_experiencia (int): Identificador único del rango.
        descripcion_rango (str): Descripción del rango de experiencia.
        experiencias (List[ExperienciaLaboral]): Relación con registros de experiencia laboral.
    """
    __tablename__ = "rangos_experiencia"

    id_rango_experiencia = Column(Integer, primary_key=True, index=True)
    descripcion_rango = Column(String(50), nullable=False, unique=True)

    # Relación con la tabla de experiencia laboral
    experiencias = relationship("ExperienciaLaboral", back_populates="rango_experiencia")
