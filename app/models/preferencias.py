"""Modelos para las preferencias laborales, disponibilidad y condiciones del candidato."""

from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Disponibilidad(Base):
    """
    Representa las opciones de disponibilidad inmediata para trabajar.

    Atributos:
        id_disponibilidad (int): Identificador único.
        descripcion_disponibilidad (str): Descripción de la disponibilidad.
        preferencias (List[PreferenciaDisponibilidad]): Preferencias laborales asociadas.
    """
    __tablename__ = "disponibilidad"

    id_disponibilidad = Column(Integer, primary_key=True, index=True)
    descripcion_disponibilidad = Column(String(50), nullable=False, unique=True)

    preferencias = relationship(
        "PreferenciaDisponibilidad", back_populates="disponibilidad"
    )


class RangoSalarial(Base):
    """
    Representa los rangos salariales deseados por los candidatos.

    Atributos:
        id_rango_salarial (int): Identificador único.
        descripcion_rango (str): Descripción del rango salarial.
        preferencias (List[PreferenciaDisponibilidad]): Preferencias laborales asociadas.
    """
    __tablename__ = "rangos_salariales"

    id_rango_salarial = Column(Integer, primary_key=True, index=True)
    descripcion_rango = Column(String(50), nullable=False, unique=True)

    preferencias = relationship(
        "PreferenciaDisponibilidad", back_populates="rango_salarial"
    )


class MotivoSalida(Base):
    """
    Representa los motivos por los cuales un candidato dejó un trabajo anterior.

    Atributos:
        id_motivo_salida (int): Identificador único.
        descripcion_motivo (str): Descripción del motivo.
        preferencias (List[PreferenciaDisponibilidad]): Preferencias laborales asociadas.
        candidato (Candidato): Candidato que reportó este motivo.
    """
    __tablename__ = "motivos_salida"

    id_motivo_salida = Column(Integer, primary_key=True, index=True)
    descripcion_motivo = Column(String(100), nullable=False, unique=True)

    preferencias = relationship(
        "PreferenciaDisponibilidad", back_populates="motivo_salida"
    )
    candidato = relationship("Candidato", back_populates="motivo_salida")


class PreferenciaDisponibilidad(Base):
    """
    Representa las preferencias y condiciones laborales declaradas por el candidato.

    Atributos:
        id_preferencia (int): Identificador único de la preferencia.
        id_candidato (int): Clave foránea al candidato.
        disponibilidad_viajar (bool): Indica si el candidato puede viajar.
        id_disponibilidad_inicio (int): Clave foránea a la disponibilidad de inicio.
        id_rango_salarial (int): Clave foránea al rango salarial esperado.
        trabaja_actualmente (bool): Indica si el candidato está actualmente trabajando.
        id_motivo_salida (int): Clave foránea al motivo de salida (opcional).
        razon_trabajar_joyco (str): Justificación del candidato para querer trabajar en Joyco.

    Relaciones:
        disponibilidad (Disponibilidad): Disponibilidad de inicio.
        rango_salarial (RangoSalarial): Rango salarial esperado.
        motivo_salida (MotivoSalida): Motivo por el cual dejó un empleo anterior.
        candidato (Candidato): Candidato asociado a estas preferencias.
    """
    __tablename__ = "preferencias_disponibilidad"

    id_preferencia = Column(Integer, primary_key=True, index=True)
    id_candidato = Column(
        Integer, ForeignKey("candidatos.id_candidato"), nullable=False
    )
    disponibilidad_viajar = Column(Boolean, nullable=False)
    id_disponibilidad_inicio = Column(
        Integer, ForeignKey("disponibilidad.id_disponibilidad"), nullable=False
    )
    id_rango_salarial = Column(
        Integer, ForeignKey("rangos_salariales.id_rango_salarial"), nullable=False
    )
    trabaja_actualmente = Column(Boolean, nullable=False)
    id_motivo_salida = Column(
        Integer, ForeignKey("motivos_salida.id_motivo_salida"), nullable=True
    )
    razon_trabajar_joyco = Column(Text, nullable=True)

    disponibilidad = relationship("Disponibilidad", back_populates="preferencias")
    rango_salarial = relationship("RangoSalarial", back_populates="preferencias")
    motivo_salida = relationship("MotivoSalida", back_populates="preferencias")
    candidato = relationship("Candidato", back_populates="preferencias")
