from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base


# Modelo de Habilidades Blandas
class HabilidadBlanda(Base):
    __tablename__ = "habilidades_blandas"

    id_habilidad_blanda = Column(Integer, primary_key=True, index=True)
    nombre_habilidad_blanda = Column(String(100), unique=True, nullable=False)


# Modelo de Habilidades Técnicas
class HabilidadTecnica(Base):
    __tablename__ = "habilidades_tecnicas"

    id_habilidad_tecnica = Column(Integer, primary_key=True, index=True)
    nombre_habilidad_tecnica = Column(String(100), unique=True, nullable=False)


# Modelo de Herramientas
class Herramienta(Base):
    __tablename__ = "herramientas"

    id_herramienta = Column(Integer, primary_key=True, index=True)
    nombre_herramienta = Column(String(100), unique=True, nullable=False)


# Modelo de Conocimientos por el candidato
class CandidatoConocimiento(Base):
    __tablename__ = "candidato_conocimientos"

    id_conocimiento = Column(Integer, primary_key=True, index=True)
    id_candidato = Column(
        Integer,
        ForeignKey("candidatos.id_candidato", ondelete="CASCADE"),
        nullable=False,
    )
    tipo_conocimiento = Column(String(50), nullable=False)
    id_habilidad_blanda = Column(
        Integer,
        ForeignKey("habilidades_blandas.id_habilidad_blanda", ondelete="CASCADE"),
        nullable=True,
    )
    id_habilidad_tecnica = Column(
        Integer,
        ForeignKey("habilidades_tecnicas.id_habilidad_tecnica", ondelete="CASCADE"),
        nullable=True,
    )
    id_herramienta = Column(
        Integer,
        ForeignKey("herramientas.id_herramienta", ondelete="CASCADE"),
        nullable=True,
    )

    # Restricción de tipo_conocimiento dentro de __table_args__
    __table_args__ = (
        CheckConstraint(
            "tipo_conocimiento IN ('blanda', 'tecnica', 'herramienta')",
            name="chk_tipo_conocimiento",
        ),
    )

    # Relaciones
    habilidad_blanda = relationship("HabilidadBlanda")
    habilidad_tecnica = relationship("HabilidadTecnica")
    herramienta = relationship("Herramienta")

    # Relaciones con Candidato
    candidato = relationship("Candidato", back_populates="conocimientos")
