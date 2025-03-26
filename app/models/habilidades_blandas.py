from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


#  Modelo para la tabla de Habilidades Blandas
class HabilidadBlanda(Base):
    __tablename__ = "habilidades_blandas"

    id_habilidad_blanda = Column(Integer, primary_key=True, index=True)
    nombre_habilidad = Column(String(100), nullable=False, unique=True)

    # Relación con Habilidades Blandas por Candidato
    habilidades_candidatos = relationship("HabilidadBlandaCandidato", back_populates="habilidad_blanda")


#  Modelo para la tabla de Habilidades Blandas por Candidato
class HabilidadBlandaCandidato(Base):
    __tablename__ = "habilidades_blandas_candidato"

    id = Column(Integer, primary_key=True, index=True)
    id_candidato = Column(Integer, ForeignKey("candidatos.id_candidato"), nullable=False)
    id_habilidad_blanda = Column(Integer, ForeignKey("habilidades_blandas.id_habilidad_blanda"), nullable=False)

    # Relación con Habilidad Blanda
    habilidad_blanda = relationship("HabilidadBlanda", back_populates="habilidades_candidatos")

    # Relacion Inversa con Candidatos
    candidato = relationship ("Candidato", back_populates="habilidades_blandas")  
    
    