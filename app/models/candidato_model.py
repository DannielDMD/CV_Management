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
        trabaja_actualmente_joyco (bool): Indica si actualmente trabaja en Joyco.
        ha_trabajado_joyco (bool): Indica si ha trabajado previamente en Joyco.
        id_motivo_salida (int): Clave foránea al motivo de salida (si aplica).
        tiene_referido (bool): Indica si fue referido por alguien.
        nombre_referido (str): Nombre del referido, si aplica.
        fecha_registro (timestamp): Fecha de registro del candidato.
        estado (str): Estado del proceso (ej. EN_PROCESO, ADMITIDO, DESCARTADO).
        formulario_completo (bool): Indica si completó todo el formulario.
        acepta_politica_datos (bool): Indica si aceptó la política de datos.

    Relaciones:
        ciudad (Ciudad): Ciudad asociada.
        cargo (CargoOfrecido): Cargo al que aplica.
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
    trabaja_actualmente_joyco = Column(Boolean, nullable=False)
    ha_trabajado_joyco = Column(Boolean, nullable=False)
    id_motivo_salida = Column(
        Integer, ForeignKey("motivos_salida.id_motivo_salida"), nullable=True
    )
    tiene_referido = Column(Boolean, nullable=False)
    nombre_referido = Column(String(255), nullable=True)
    fecha_registro = Column(TIMESTAMP, server_default=func.current_timestamp())
    estado = Column(String(20), nullable=False, default="EN_PROCESO")
    formulario_completo = Column(Boolean, nullable=False, default=False)
    acepta_politica_datos = Column(Boolean, nullable=False, default=False)

    # Relaciones con catálogos
    ciudad = relationship("Ciudad", back_populates="candidatos")
    cargo = relationship("CargoOfrecido", back_populates="candidatos")
    motivo_salida = relationship("MotivoSalida", back_populates="candidato")

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
