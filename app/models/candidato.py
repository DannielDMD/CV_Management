from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, Date, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
#from app.models.catalogs.ciudad import *
#from app.schemas.catalogs.cargo_ofrecido import *
#from app.schemas.catalogs.categoria_cargo import *
#from app.models.catalogs.categoria_cargo import *
#from app.models.catalogs.cargo_ofrecido import *

class Candidato(Base):
    __tablename__ = "candidatos"

    id_candidato = Column(Integer, primary_key=True, index=True)
    nombre_completo = Column(String(150), nullable=False)
    correo_electronico = Column(String(100), nullable=False, unique=True)
    cc = Column(String(20), nullable=False, unique=True)
    fecha_nacimiento = Column(Date, nullable=True)
    telefono = Column(String(20), nullable=False)
    id_ciudad = Column(Integer, ForeignKey("ciudades.id_ciudad"), nullable=False)
    descripcion_perfil = Column(Text, nullable=True)
    #id_categoria_cargo = Column(Integer, ForeignKey("categoria_cargos.id_categoria"), nullable=False)
    id_cargo = Column(Integer, ForeignKey("cargos_ofrecidos.id_cargo"), nullable=False)
    trabaja_actualmente_joyco = Column(Boolean, nullable=False)
    ha_trabajado_joyco = Column(Boolean, nullable=False)
    id_motivo_salida = Column(Integer, ForeignKey("motivos_salida.id_motivo_salida"), nullable=True)
    tiene_referido = Column(Boolean, nullable=False)
    nombre_referido = Column(String(150), nullable=True)
    fecha_registro = Column(TIMESTAMP, server_default=func.now())

    # Relaciones con otras tablas
    ciudad = relationship("Ciudad", back_populates="candidatos")
    #categoria_cargo = relationship("CategoriaCargo", back_populates="candidatos")
    cargo = relationship("CargoOfrecido", back_populates="candidatos")
    motivo_salida = relationship("MotivoSalida", back_populates="candidato")
    
    #Relaciones Inversas con las demás tablas generales
    educaciones = relationship ("Educacion", back_populates="candidato", cascade="all, delete-orphan")
    experiencias = relationship ("ExperienciaLaboral", back_populates="candidato", cascade="all, delete-orphan")
    habilidades_tecnicas = relationship ("HabilidadTecnicaCandidato", back_populates="candidato", cascade="all, delete-orphan")
    habilidades_blandas = relationship ("HabilidadBlandaCandidato", back_populates="candidato", cascade="all, delete-orphan")
    herramientas = relationship ( "HerramientaCandidato", back_populates="candidato", cascade="all, delete-orphan")
    preferencias = relationship ("PreferenciaDisponibilidad", back_populates="candidato", cascade="all, delete-orphan")