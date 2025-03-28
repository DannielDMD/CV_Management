"""from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class EstadoCivil(Base):
    __tablename__ = "estado_civil"

    id_estado_civil = Column(Integer, primary_key=True, index=True)
    nombre_estado_civil = Column(String(50), unique=True, nullable=False)

    # Relación inversa con Candidatos (nombre correcto)
    candidatos = relationship("Candidato", back_populates="estado")  

"""