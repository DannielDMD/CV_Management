from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

# Modelo para definir el nivel de Educación 
class NivelEducacion(Base):
    __tablename__ = "nivel_educacion"
    
    id_nivel_educacion = Column(Integer, primary_key=True, index=True)
    descripcion_nivel = Column(String(100), nullable=False, unique=True)
    
    # Relación con Educación (si aún se requiere en el futuro)
    educaciones = relationship("Educacion", back_populates="nivel_educacion")
    titulos = relationship("TituloObtenido", back_populates="nivel_educacion")