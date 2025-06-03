"""Modelo de la tabla 'candidatos'."""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    Text,
    Date,
    TIMESTAMP,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Candidato(Base):
    """
    Representa un candidato registrado en el sistema de gestión.

    Atributos:
        id_candidato (int): Identificador único del candidato.
        nombre_completo (str): Nombre completo del candidato.
        correo_electronico (str): Correo electrónico único.
        cc (str): Cédula de ciudadanía única.
        fecha_nacimiento (date): Fecha de nacimiento del candidato.
        telefono (str): Número de contacto.
        id_ciudad (int): Clave foránea a la ciudad de residencia.
        descripcion_perfil (str): Descripción libre del perfil profesional.
        id_cargo (int): Clave foránea al cargo ofrecido.
        nombre_cargo_otro (str): Texto libre si el cargo no está en el catálogo.
        trabaja_actualmente_joyco (bool): Indica si actualmente trabaja en Joyco.
        ha_trabajado_joyco (bool): Indica si ha trabajado previamente en Joyco.
        id_motivo_salida (int): Clave foránea al motivo de salida (si aplica).
        otro_motivo_salida (str): Texto libre si el motivo no está en el catálogo.
        tiene_referido (bool): Indica si fue referido por alguien.
        nombre_referido (str): Nombre del referido, si aplica.
        id_centro_costos (int): Clave foránea al centro de costos (si aplica).
        nombre_centro_costos_otro (str): Texto libre si el centro de costos no está en el catálogo.
        fecha_registro (timestamp): Fecha de registro del candidato.
        estado (str): Estado del proceso (ej. EN_PROCESO, ADMITIDO, DESCARTADO).
        formulario_completo (bool): Indica si completó todo el formulario.
        acepta_politica_datos (bool): Indica si aceptó la política de datos.

    Relaciones:
        ciudad (Ciudad): Ciudad asociada.
        cargo (CargoOfrecido): Cargo al que aplica.
        centros_costos (CentroCostos): Centro de Costos en el que está, si actualmente trabaja en Joyco
        motivo_salida (MotivoSalida): Motivo de salida si trabajó en Joyco.
        educaciones (List[Educacion]): Registros de educación asociados.
        experiencias (List[ExperienciaLaboral]): Registros de experiencia.
        conocimientos (List[CandidatoConocimiento]): Conocimientos técnicos/blandos.
        preferencias (List[PreferenciaDisponibilidad]): Preferencias laborales.
    """
    __tablename__ = "candidatos"

    id_candidato = Column(Integer, primary_key=True, index=True)
    nombre_completo = Column(String(255), nullable=False)
    correo_electronico = Column(String(150), unique=True, nullable=False)
    cc = Column(String(20), unique=True, nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    telefono = Column(String(20), nullable=False)
    id_ciudad = Column(Integer, ForeignKey("ciudades.id_ciudad"), nullable=False)
    descripcion_perfil = Column(Text)
    id_cargo = Column(Integer, ForeignKey("cargos_ofrecidos.id_cargo"), nullable=False)
    nombre_cargo_otro = Column(String(100), nullable=True)
    trabaja_actualmente_joyco = Column(Boolean, nullable=False)
    ha_trabajado_joyco = Column(Boolean, nullable=False)
    id_motivo_salida = Column(Integer, ForeignKey("motivos_salida.id_motivo_salida"), nullable=True)
    otro_motivo_salida = Column(Text, nullable=True)
    tiene_referido = Column(Boolean, nullable=False)
    nombre_referido = Column(String(255), nullable=True)
    id_centro_costos = Column(Integer, ForeignKey("centros_costos.id_centro_costos"), nullable=True)
    nombre_centro_costos_otro = Column(String(150), nullable=True)
    fecha_registro = Column(TIMESTAMP, server_default=func.current_timestamp())
    estado = Column(String(20), nullable=False, default="EN_PROCESO")
    formulario_completo = Column(Boolean, nullable=False, default=False)
    acepta_politica_datos = Column(Boolean, nullable=False, default=False)

    # Relaciones con catálogos
    ciudad = relationship("Ciudad", back_populates="candidatos")
    cargo = relationship("CargoOfrecido", back_populates="candidatos")
    motivo_salida = relationship("MotivoSalida", back_populates="candidato")
    centro_costos = relationship("CentroCostos", back_populates="candidatos")


    # Relaciones con tablas dependientes
    educaciones = relationship(
        "Educacion", back_populates="candidato", cascade="all, delete-orphan"
    )
    experiencias = relationship(
        "ExperienciaLaboral", back_populates="candidato", cascade="all, delete-orphan"
    )
    conocimientos = relationship(
        "CandidatoConocimiento", back_populates="candidato", cascade="all, delete-orphan"
    )
    preferencias = relationship(
        "PreferenciaDisponibilidad", back_populates="candidato", cascade="all, delete-orphan"
    )
