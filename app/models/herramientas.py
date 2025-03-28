"""from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


#  Modelo para la tabla de Categorías de Herramientas
class CategoriaHerramienta(Base):
    __tablename__ = "categorias_herramientas"

    id_categoria_herramienta = Column(Integer, primary_key=True, index=True)
    nombre_categoria = Column(String(100), nullable=False, unique=True)

    # Relación con Herramientas
    herramientas = relationship("Herramienta", back_populates="categoria")


#  Modelo para la tabla de Herramientas
class Herramienta(Base):
    __tablename__ = "herramientas"

    id_herramienta = Column(Integer, primary_key=True, index=True)
    nombre_herramienta = Column(String(100), nullable=False)
    id_categoria_herramienta = Column(
        Integer,
        ForeignKey("categorias_herramientas.id_categoria_herramienta"),
        nullable=False,
    )

    # Relación con Categoría de Herramientas
    categoria = relationship("CategoriaHerramienta", back_populates="herramientas")

    # Relación inversa con HerramientaCandidato
    candidatos = relationship("HerramientaCandidato", back_populates="herramienta")


#  Modelo para la tabla de Herramientas por Candidato (Tabla Intermedia)
class HerramientaCandidato(Base):
    __tablename__ = "herramientas_candidato"

    id = Column(Integer, primary_key=True, index=True)
    id_candidato = Column(
        Integer, ForeignKey("candidatos.id_candidato"), nullable=False
    )
    id_herramienta = Column(
        Integer, ForeignKey("herramientas.id_herramienta"), nullable=False
    )

    # Relación con Candidato
    candidato = relationship("Candidato", back_populates="herramientas")

    # Relación con Herramienta
    herramienta = relationship("Herramienta", back_populates="candidatos")
"""