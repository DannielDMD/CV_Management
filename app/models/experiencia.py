from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

#  Modelo para la tabla de Rangos de Experiencia
class RangoExperiencia(Base):
    __tablename__ = "rangos_experiencia"

    id_rango_experiencia = Column(Integer, primary_key=True, index=True)
    descripcion_rango = Column(String(50), nullable=False, unique=True)

    # Relación con Experiencia Laboral
    experiencias = relationship("ExperienciaLaboral", back_populates="rango_experiencia")


# 🏢 Modelo para la tabla de Experiencia Laboral
class ExperienciaLaboral(Base):
    __tablename__ = "experiencia_laboral"

    id_experiencia = Column(Integer, primary_key=True, index=True)
    id_candidato = Column(Integer, ForeignKey("candidatos.id_candidato"), nullable=False)
    id_rango_experiencia = Column(Integer, ForeignKey("rangos_experiencia.id_rango_experiencia"), nullable=False)
    ultima_empresa = Column(String(150), nullable=False)
    ultimo_cargo = Column(String(100), nullable=False)
    funciones = Column(Text, nullable=True)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=True)

    # Relaciones
    rango_experiencia = relationship("RangoExperiencia", back_populates="experiencias")
    
    #Relaciones con candidatos
    candidato = relationship ("Candidato", back_populates="experiencias")
