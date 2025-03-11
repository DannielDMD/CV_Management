from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class NivelIngles(Base):
    __tablename__ = "nivel_ingles"

    id_nivel_ingles = Column(Integer, primary_key=True, index=True)
    nivel = Column(String(20), nullable=False, unique=True)

    # Relación con Educación
    educaciones = relationship("Educacion", back_populates="nivel_ingles")
