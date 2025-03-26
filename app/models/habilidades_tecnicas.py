from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


#  Modelo para la tabla de Categorías de Habilidades Técnicas
class CategoriaHabilidadTecnica(Base):
    __tablename__ = "categorias_habilidades_tecnicas"

    id_categoria_habilidad = Column(Integer, primary_key=True, index=True)
    nombre_categoria = Column(String(100), nullable=False, unique=True)

    # Relación con Habilidades Técnicas
    habilidades_tecnicas = relationship("HabilidadTecnica", back_populates="categoria")


#  Modelo para la tabla de Habilidades Técnicas
class HabilidadTecnica(Base):
    __tablename__ = "habilidades_tecnicas"

    id_habilidad_tecnica = Column(Integer, primary_key=True, index=True)
    nombre_habilidad = Column(String(100), nullable=False)
    id_categoria_habilidad = Column(
        Integer,
        ForeignKey("categorias_habilidades_tecnicas.id_categoria_habilidad"),
        nullable=False,
    )

    # Relación con Categoría de Habilidades Técnicas
    categoria = relationship(
        "CategoriaHabilidadTecnica", back_populates="habilidades_tecnicas"
    )

    # Relación inversa con HabilidadTecnicaCandidato
    candidatos = relationship(
        "HabilidadTecnicaCandidato", back_populates="habilidad_tecnica"
    )


#  Modelo para la tabla de Habilidades Técnicas por Candidato
class HabilidadTecnicaCandidato(Base):
    __tablename__ = "habilidades_tecnicas_candidato"

    id = Column(Integer, primary_key=True, index=True)
    id_candidato = Column(
        Integer, ForeignKey("candidatos.id_candidato"), nullable=False
    )
    id_habilidad_tecnica = Column(
        Integer, ForeignKey("habilidades_tecnicas.id_habilidad_tecnica"), nullable=False
    )

    # Relacion Inversa con Candidatos
    candidato = relationship("Candidato", back_populates="habilidades_tecnicas")

    # Relación con HabilidadTecnica
    habilidad_tecnica = relationship("HabilidadTecnica", back_populates="candidatos")
