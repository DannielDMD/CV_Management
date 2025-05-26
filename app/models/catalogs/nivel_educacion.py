"""Modelo de la tabla 'nivel_educacion'."""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class NivelEducacion(Base):
    """
    Representa los niveles de educación registrados (ej. Primaria, Secundaria, Universitaria).

    Atributos:
        id_nivel_educacion (int): Identificador único del nivel educativo.
        descripcion_nivel (str): Descripción textual del nivel.
        educaciones (List[Educacion]): Relación con registros de educación de los candidatos.
        titulos (List[TituloObtenido]): Relación con los títulos obtenidos asociados a este nivel.
    """
    __tablename__ = "nivel_educacion"
    
    id_nivel_educacion = Column(Integer, primary_key=True, index=True)
    descripcion_nivel = Column(String(100), nullable=False, unique=True)
    
    # Relaciones con otras tablas
    educaciones = relationship("Educacion", back_populates="nivel_educacion")
    titulos = relationship("TituloObtenido", back_populates="nivel_educacion")
