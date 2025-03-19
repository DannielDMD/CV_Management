from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class CargoOfrecido(Base):
    __tablename__ = "cargos_ofrecidos"

    id_cargo = Column(Integer, primary_key=True, index=True)
    nombre_cargo = Column(String(100), nullable=False, unique=True)
    """id_categoria = Column(Integer, ForeignKey("categoria_cargos.id_categoria"), nullable=False)"""

     # Relación con Categoría de Cargos
    """categoria = relationship("CategoriaCargo", back_populates="cargos")"""
    candidatos = relationship("Candidato", back_populates="cargo")
