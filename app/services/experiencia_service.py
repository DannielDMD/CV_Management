from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.experiencia_model import ExperienciaLaboral
from app.schemas.experiencia_schema import (
    ExperienciaLaboralCreate,
    ExperienciaLaboralUpdate,
)
from app.utils.orden_catalogos import ordenar_por_nombre

# ─────────────────────────────────────────────────────────────────────────────
# SERVICIO: Gestión de la experiencia laboral de los candidatos
# ─────────────────────────────────────────────────────────────────────────────

def create_experiencia(db: Session, experiencia_data: ExperienciaLaboralCreate):
    """
    Crea un nuevo registro de experiencia laboral.

    Args:
        db (Session): Sesión activa de la base de datos.
        experiencia_data (ExperienciaLaboralCreate): Datos para la creación.

    Returns:
        ExperienciaLaboral: Objeto creado y persistido.

    Raises:
        HTTPException: Si ocurre un error de integridad en la base de datos.
    """
    nueva_experiencia = ExperienciaLaboral(**experiencia_data.model_dump())
    try:
        db.add(nueva_experiencia)
        db.commit()
        db.refresh(nueva_experiencia)
        return nueva_experiencia
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Error al insertar la experiencia laboral en la base de datos",
        )


def get_experiencia_by_id(db: Session, id_experiencia: int):
    """
    Obtiene una experiencia laboral por su ID.

    Args:
        db (Session): Sesión activa de la base de datos.
        id_experiencia (int): ID de la experiencia.

    Returns:
        ExperienciaLaboral: Registro encontrado.

    Raises:
        HTTPException: Si no se encuentra la experiencia.
    """
    experiencia = (
        db.query(ExperienciaLaboral)
        .filter(ExperienciaLaboral.id_experiencia == id_experiencia)
        .first()
    )

    if not experiencia:
        raise HTTPException(status_code=404, detail="Experiencia laboral no encontrada")

    return experiencia


def get_experiencias_by_candidato(db: Session, id_candidato: int):
    """
    Obtiene todas las experiencias laborales asociadas a un candidato.

    Args:
        db (Session): Sesión activa.
        id_candidato (int): ID del candidato.

    Returns:
        List[ExperienciaLaboral]: Lista de experiencias.

    Raises:
        HTTPException: Si no se encuentran registros.
    """
    experiencias = (
        db.query(ExperienciaLaboral)
        .filter(ExperienciaLaboral.id_candidato == id_candidato)
        .all()
    )

    if not experiencias:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron experiencias laborales para este candidato",
        )

    return experiencias


def get_all_experiencias(db: Session):
    """
    Obtiene todos los registros de experiencia laboral existentes.

    Args:
        db (Session): Sesión activa.

    Returns:
        List[ExperienciaLaboral]: Lista completa de experiencias.
    """
    return db.query(ExperienciaLaboral).all()


def update_experiencia(
    db: Session, id_experiencia: int, experiencia_data: ExperienciaLaboralUpdate
):
    """
    Actualiza los datos de una experiencia laboral.

    Args:
        db (Session): Sesión activa.
        id_experiencia (int): ID de la experiencia.
        experiencia_data (ExperienciaLaboralUpdate): Campos a actualizar.

    Returns:
        ExperienciaLaboral: Registro actualizado.

    Raises:
        HTTPException: Si el registro no existe.
    """
    experiencia = (
        db.query(ExperienciaLaboral)
        .filter(ExperienciaLaboral.id_experiencia == id_experiencia)
        .first()
    )

    if not experiencia:
        raise HTTPException(status_code=404, detail="Experiencia laboral no encontrada")

    for key, value in experiencia_data.model_dump(exclude_unset=True).items():
        setattr(experiencia, key, value)

    db.commit()
    db.refresh(experiencia)

    return experiencia


def delete_experiencia(db: Session, id_experiencia: int):
    """
    Elimina una experiencia laboral de la base de datos.

    Args:
        db (Session): Sesión activa.
        id_experiencia (int): ID de la experiencia a eliminar.

    Returns:
        dict: Mensaje de confirmación.

    Raises:
        HTTPException: Si el registro no existe.
    """
    experiencia = (
        db.query(ExperienciaLaboral)
        .filter(ExperienciaLaboral.id_experiencia == id_experiencia)
        .first()
    )

    if not experiencia:
        raise HTTPException(status_code=404, detail="Experiencia laboral no encontrada")

    db.delete(experiencia)
    db.commit()

    return {"message": "Experiencia laboral eliminada correctamente"}
