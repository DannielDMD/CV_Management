# app/core/init_db.py
from app.core.database import Base, engine
from .populate_catalogs import cargar_catalogos

# Importar modelos generales
from app.models import (
    Candidato,
    Educacion,
    ExperienciaLaboral,
    CandidatoConocimiento,
    PreferenciaDisponibilidad,
    Usuario,
    SolicitudEliminacion,
)

# Importar modelos de catálogos
from app.models import (
    HabilidadBlanda,
    HabilidadTecnica,
    Herramienta,
    Disponibilidad,
    RangoSalarial,
    MotivoSalida,
)

from app.models.catalogs import (
    Departamento,
    Ciudad,
    CargoOfrecido,
    CentroCostos,
    NivelEducacion,
    TituloObtenido,
    InstitucionAcademica,
    NivelIngles,
    RangoExperiencia,
)

def create_tables():
    """Crea todas las tablas si no existen en la base de datos."""
    Base.metadata.create_all(bind=engine)

def init_db():
    """Inicializa la base de datos completa (creación de tablas)."""
    create_tables()
    cargar_catalogos()
