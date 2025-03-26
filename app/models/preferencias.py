from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


# Modelo para la tabla de Disponibilidad
class Disponibilidad(Base):
    __tablename__ = "disponibilidad"

    id_disponibilidad = Column(Integer, primary_key=True, index=True)
    descripcion_disponibilidad = Column(String(50), nullable=False, unique=True)

    # Relación con Preferencias y Disponibilidad
    preferencias = relationship(
        "PreferenciaDisponibilidad", back_populates="disponibilidad"
    )


#  Modelo para la tabla de Rangos Salariales
class RangoSalarial(Base):
    __tablename__ = "rangos_salariales"

    id_rango_salarial = Column(Integer, primary_key=True, index=True)
    descripcion_rango = Column(String(50), nullable=False, unique=True)

    # Relación con Preferencias y Disponibilidad
    preferencias = relationship(
        "PreferenciaDisponibilidad", back_populates="rango_salarial"
    )


# Modelo para la tabla de Motivos de Salida
class MotivoSalida(Base):
    __tablename__ = "motivos_salida"

    id_motivo_salida = Column(Integer, primary_key=True, index=True)
    descripcion_motivo = Column(String(100), nullable=False, unique=True)

    # Relación con Preferencias y Disponibilidad
    preferencias = relationship(
        "PreferenciaDisponibilidad", back_populates="motivo_salida"
    )
    # Relación con candidatos
    candidato = relationship("Candidato", back_populates="motivo_salida")


#  Modelo para la tabla de Preferencias y Disponibilidad
class PreferenciaDisponibilidad(Base):
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

    # Relaciones
    disponibilidad = relationship("Disponibilidad", back_populates="preferencias")
    rango_salarial = relationship("RangoSalarial", back_populates="preferencias")
    motivo_salida = relationship("MotivoSalida", back_populates="preferencias")

    # Relaciones con Candidato
    candidato = relationship("Candidato", back_populates="preferencias")
