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
    
    # ✅ Nuevo campo: estado del candidato
    estado = Column(String(20), nullable=False, default="EN_PROCESO")

    # SE CREA EL NUEVO CAMPO PARA SABER SI SE COMPLETÓ O NO EL FORMULARIO
    formulario_completo = Column(Boolean, nullable=False, default=False)  # ✅ nuevo campo

    # SE CREA EL NUEVO CAMPO PARA CUANDO SE ACEPTA LA POLITICA DE DATOS
    acepta_politica_datos = Column(Boolean, nullable=False, default=False)

    
    
    
    # Relaciones con otras tablas
    ciudad = relationship("Ciudad", back_populates="candidatos")
    cargo = relationship("CargoOfrecido", back_populates="candidatos")
    motivo_salida = relationship("MotivoSalida", back_populates="candidato")

    # Relaciones inversas con tablas dependientes
    educaciones = relationship(
        "Educacion", back_populates="candidato", cascade="all, delete-orphan"
    )
    experiencias = relationship(
        "ExperienciaLaboral", back_populates="candidato", cascade="all, delete-orphan"
    )
    conocimientos = relationship(
        "CandidatoConocimiento",
        back_populates="candidato",
        cascade="all, delete-orphan",
    )

    preferencias = relationship(
        "PreferenciaDisponibilidad",
        back_populates="candidato",
        cascade="all, delete-orphan",
    )
