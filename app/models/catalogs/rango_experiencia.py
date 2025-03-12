from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base
from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship
from app.core.database import Base

#  Modelo para la tabla de Rangos de Experiencia
class RangoExperiencia(Base):
    __tablename__ = "rangos_experiencia"

    id_rango_experiencia = Column(Integer, primary_key=True, index=True)
    descripcion_rango = Column(String(50), nullable=False, unique=True)

    # Relación con Experiencia Laboral
    experiencias = relationship("ExperienciaLaboral", back_populates="rango_experiencia")

