from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class Ciudad(Base):
    __tablename__ = "ciudades"

    id_ciudad = Column(Integer, primary_key=True, index=True)
    nombre_ciudad = Column(String(100), nullable=False, unique=True)

    # Relación inversa con Candidatos
    candidatos = relationship("Candidato", back_populates="ciudad")
