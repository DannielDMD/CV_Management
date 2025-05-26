"""
Servicios para gestionar el catálogo de Niveles de Educación.
Incluye operaciones CRUD: listar, obtener, crear, actualizar y eliminar.
"""

from sqlalchemy.orm import Session
from app.models.catalogs.nivel_educacion import NivelEducacion
from app.schemas.catalogs.nivel_educacion import NivelEducacionCreate, NivelEducacionUpdate


def get_niveles_educacion(db: Session, skip: int = 0, limit: int = 10):
    """
    Obtiene una lista paginada de niveles de educación.

    Args:
        db (Session): Sesión activa de la base de datos.
        skip (int): Número de elementos a omitir (para paginación).
        limit (int): Número máximo de elementos a retornar.

    Returns:
        List[NivelEducacion]: Lista de niveles de educación.
    """
    return db.query(NivelEducacion).offset(skip).limit(limit).all()


def get_nivel_educacion(db: Session, id_nivel_educacion: int):
    """
    Obtiene un nivel de educación por su ID.

    Args:
        db (Session): Sesión activa de la base de datos.
        id_nivel_educacion (int): ID del nivel a consultar.

    Returns:
        NivelEducacion | None: Objeto encontrado o None si no existe.
    """
    return db.query(NivelEducacion).filter(
        NivelEducacion.id_nivel_educacion == id_nivel_educacion
    ).first()


def create_nivel_educacion(db: Session, nivel_educacion_data: NivelEducacionCreate):
    """
    Crea un nuevo nivel de educación.

    Args:
        db (Session): Sesión activa de la base de datos.
        nivel_educacion_data (NivelEducacionCreate): Datos del nuevo nivel.

    Returns:
        NivelEducacion: Objeto creado.
    """
    nuevo_nivel = NivelEducacion(**nivel_educacion_data.model_dump())
    db.add(nuevo_nivel)
    db.commit()
    db.refresh(nuevo_nivel)
    return nuevo_nivel


def update_nivel_educacion(db: Session, id_nivel_educacion: int, nivel_educacion_data: NivelEducacionUpdate):
    """
    Actualiza un nivel de educación existente.

    Args:
        db (Session): Sesión activa de la base de datos.
        id_nivel_educacion (int): ID del nivel a actualizar.
        nivel_educacion_data (NivelEducacionUpdate): Campos a modificar.

    Returns:
        NivelEducacion | None: Nivel actualizado o None si no existe.
    """
    nivel = db.query(NivelEducacion).filter(
        NivelEducacion.id_nivel_educacion == id_nivel_educacion
    ).first()
    if not nivel:
        return None

    for key, value in nivel_educacion_data.model_dump(exclude_unset=True).items():
        setattr(nivel, key, value)

    db.commit()
    db.refresh(nivel)
    return nivel


def delete_nivel_educacion(db: Session, id_nivel_educacion: int):
    """
    Elimina un nivel de educación por su ID.

    Args:
        db (Session): Sesión activa de la base de datos.
        id_nivel_educacion (int): ID del nivel a eliminar.

    Returns:
        NivelEducacion | None: Nivel eliminado o None si no existe.
    """
    nivel = db.query(NivelEducacion).filter(
        NivelEducacion.id_nivel_educacion == id_nivel_educacion
    ).first()
    if not nivel:
        return None

    db.delete(nivel)
    db.commit()
    return nivel
