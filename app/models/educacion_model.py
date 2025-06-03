"""Modelo de la tabla 'educacion'."""

from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class Educacion(Base):
    """
    Representa un registro educativo asociado a un candidato.

    Atributos:
        id_educacion (int): Identificador único del registro educativo.
        id_candidato (int): Clave foránea al candidato.
        id_nivel_educacion (int): Clave foránea al nivel educativo alcanzado.
        id_titulo (int): Clave foránea al título obtenido (opcional).
        id_institucion (int): Clave foránea a la institución académica (opcional).
        anio_graduacion (int): Año de graduación del programa educativo.
        id_nivel_ingles (int): Clave foránea al nivel de inglés del candidato.
        nombre_titulo_otro (str): Título ingresado manualmente si no está en el catálogo.
        nombre_institucion_otro (str): Institución ingresada manualmente si no está en el catálogo.

    Relaciones:
        nivel_educacion (NivelEducacion): Nivel educativo alcanzado.
        titulo (TituloObtenido): Título obtenido por el candidato.
        institucion (InstitucionAcademica): Institución donde cursó estudios.
        nivel_ingles (NivelIngles): Nivel de inglés declarado.
        candidato (Candidato): Candidato asociado al registro educativo.
    """
    __tablename__ = "educacion"

    id_educacion = Column(Integer, primary_key=True, index=True)
    id_candidato = Column(
        Integer, ForeignKey("candidatos.id_candidato"), nullable=False
    )
    id_nivel_educacion = Column(
        Integer, ForeignKey("nivel_educacion.id_nivel_educacion"), nullable=False
    )
    id_titulo = Column(
        Integer, ForeignKey("titulos_obtenidos.id_titulo"), nullable=True
    )
    id_institucion = Column(
        Integer, ForeignKey("instituciones_academicas.id_institucion"), nullable=True
    )
    anio_graduacion = Column(Integer, nullable=True)
    id_nivel_ingles = Column(
        Integer, ForeignKey("nivel_ingles.id_nivel_ingles"), nullable=False
    )

    nombre_titulo_otro = Column(Text, nullable=True)
    nombre_institucion_otro = Column(Text, nullable=True)
    
    # Relaciones con tablas de catálogo
    nivel_educacion = relationship("NivelEducacion", back_populates="educaciones")
    titulo = relationship("TituloObtenido")
    institucion = relationship("InstitucionAcademica")
    nivel_ingles = relationship("NivelIngles", back_populates="educaciones")

    # Relación con la tabla de candidatos
    candidato = relationship("Candidato", back_populates="educaciones")
