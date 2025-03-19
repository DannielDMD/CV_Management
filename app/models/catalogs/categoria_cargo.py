"""from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class CategoriaCargo(Base):
    __tablename__ = "categoria_cargos"

    id_categoria = Column(Integer, primary_key=True, index=True)
    nombre_categoria = Column(String(100), nullable=False, unique=True)

     # Relación inversa con Cargos
    cargos = relationship("CargoOfrecido", back_populates="categoria")
    candidatos = relationship("Candidato", back_populates="categoria_cargo")
"""