from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

"""
#  Modelo para la tabla de Nivel de Inglés
class NivelIngles(Base):
    __tablename__ = "nivel_ingles"

    id_nivel_ingles = Column(Integer, primary_key=True, index=True)
    nivel = Column(String(20), nullable=False, unique=True)

    # Relación con Educación
    educaciones = relationship("Educacion", back_populates="nivel_ingles")

"""
#  Modelo para la tabla de Educación
class Educacion(Base):
    __tablename__ = "educacion"

    id_educacion = Column(Integer, primary_key=True, index=True)
    id_candidato = Column(Integer, ForeignKey("candidatos.id_candidato"), nullable=False)
    id_nivel_educacion = Column(Integer, ForeignKey("nivel_educacion.id_nivel_educacion"), nullable=False)
    id_titulo = Column(Integer, ForeignKey("titulos_obtenidos.id_titulo"), nullable=True)
    id_institucion = Column(Integer, ForeignKey("instituciones_academicas.id_institucion"), nullable=True)
    anio_graduacion = Column(Integer, nullable=True)
    id_nivel_ingles = Column(Integer, ForeignKey("nivel_ingles.id_nivel_ingles"), nullable=False)

    # Relaciones
    nivel_educacion = relationship("NivelEducacion", back_populates="educaciones")
    titulo = relationship("TituloObtenido")
    institucion = relationship("InstitucionAcademica")
    nivel_ingles = relationship("NivelIngles", back_populates="educaciones")

    # Relación inversa con candidatos
    candidato = relationship ("Candidato", back_populates="educaciones")

