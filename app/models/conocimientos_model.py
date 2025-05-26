"""Modelos para la gestión de conocimientos del candidato."""

from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base


class HabilidadBlanda(Base):
    """
    Representa una habilidad blanda (ej. trabajo en equipo, liderazgo).

    Atributos:
        id_habilidad_blanda (int): Identificador único.
        nombre_habilidad_blanda (str): Nombre de la habilidad blanda.
    """
    __tablename__ = "habilidades_blandas"

    id_habilidad_blanda = Column(Integer, primary_key=True, index=True)
    nombre_habilidad_blanda = Column(String(100), unique=True, nullable=False)


class HabilidadTecnica(Base):
    """
    Representa una habilidad técnica (ej. programación, análisis de datos).

    Atributos:
        id_habilidad_tecnica (int): Identificador único.
        nombre_habilidad_tecnica (str): Nombre de la habilidad técnica.
    """
    __tablename__ = "habilidades_tecnicas"

    id_habilidad_tecnica = Column(Integer, primary_key=True, index=True)
    nombre_habilidad_tecnica = Column(String(100), unique=True, nullable=False)


class Herramienta(Base):
    """
    Representa una herramienta utilizada por el candidato (ej. AutoCAD, Excel).

    Atributos:
        id_herramienta (int): Identificador único.
        nombre_herramienta (str): Nombre de la herramienta.
    """
    __tablename__ = "herramientas"

    id_herramienta = Column(Integer, primary_key=True, index=True)
    nombre_herramienta = Column(String(100), unique=True, nullable=False)


class CandidatoConocimiento(Base):
    """
    Representa el conocimiento declarado por un candidato en habilidades blandas, técnicas o herramientas.

    Atributos:
        id_conocimiento (int): Identificador único del registro.
        id_candidato (int): Clave foránea al candidato.
        tipo_conocimiento (str): Tipo del conocimiento ('blanda', 'tecnica', 'herramienta').
        id_habilidad_blanda (int): FK opcional si es una habilidad blanda.
        id_habilidad_tecnica (int): FK opcional si es una habilidad técnica.
        id_herramienta (int): FK opcional si es una herramienta.

    Restricciones:
        chk_tipo_conocimiento: Limita el campo tipo_conocimiento a valores válidos.

    Relaciones:
        candidato (Candidato): Candidato asociado.
        habilidad_blanda (HabilidadBlanda): Habilidad blanda asociada.
        habilidad_tecnica (HabilidadTecnica): Habilidad técnica asociada.
        herramienta (Herramienta): Herramienta asociada.
    """
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

    __table_args__ = (
        CheckConstraint(
            "tipo_conocimiento IN ('blanda', 'tecnica', 'herramienta')",
            name="chk_tipo_conocimiento",
        ),
    )

    # Relaciones con tablas de catálogo
    habilidad_blanda = relationship("HabilidadBlanda")
    habilidad_tecnica = relationship("HabilidadTecnica")
    herramienta = relationship("Herramienta")

    # Relación con el candidato
    candidato = relationship("Candidato", back_populates="conocimientos")
