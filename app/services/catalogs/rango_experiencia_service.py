"""
Servicios para el catálogo de Rangos de Experiencia.
Incluye funciones CRUD: listar, obtener, crear, actualizar y eliminar.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.catalogs.rango_experiencia import RangoExperiencia
from app.schemas.catalogs.rango_experiencia import RangoExperienciaCreate, RangoExperienciaUpdate


def get_rangos_experiencia(db: Session):
    """
    Retorna todos los rangos de experiencia existentes.

    Args:
        db (Session): Sesión activa de la base de datos.

    Returns:
        List[RangoExperiencia]: Lista de rangos.
    """
    return db.query(RangoExperiencia).all()


def get_rango_experiencia(db: Session, rango_experiencia_id: int):
    """
    Obtiene un rango de experiencia por su ID.

    Args:
        db (Session): Sesión activa de la base de datos.
        rango_experiencia_id (int): ID del rango.

    Returns:
        RangoExperiencia: Objeto encontrado.

    Raises:
        HTTPException: Si no se encuentra el rango.
    """
    rango = db.query(RangoExperiencia).filter(
        RangoExperiencia.id_rango_experiencia == rango_experiencia_id
    ).first()

    if not rango:
        raise HTTPException(status_code=404, detail="Rango de experiencia no encontrado")

    return rango


def create_rango_experiencia(db: Session, rango_data: RangoExperienciaCreate):
    """
    Crea un nuevo rango de experiencia si no existe uno igual.

    Args:
        db (Session): Sesión activa de la base de datos.
        rango_data (RangoExperienciaCreate): Datos del nuevo rango.

    Returns:
        RangoExperiencia: Objeto creado.

    Raises:
        HTTPException: Si ya existe un rango con la misma descripción.
    """
    existe = db.query(RangoExperiencia).filter(
        RangoExperiencia.descripcion_rango == rango_data.descripcion_rango
    ).first()

    if existe:
        raise HTTPException(status_code=400, detail="El rango de experiencia ya existe")

    nuevo_rango = RangoExperiencia(descripcion_rango=rango_data.descripcion_rango)
    db.add(nuevo_rango)
    db.commit()
    db.refresh(nuevo_rango)
    return nuevo_rango


def update_rango_experiencia(db: Session, rango_experiencia_id: int, rango_data: RangoExperienciaUpdate):
    """
    Actualiza un rango de experiencia por ID.

    Args:
        db (Session): Sesión activa de la base de datos.
        rango_experiencia_id (int): ID del rango.
        rango_data (RangoExperienciaUpdate): Datos a actualizar.

    Returns:
        RangoExperiencia: Objeto actualizado.

    Raises:
        HTTPException: Si no se encuentra el rango.
    """
    rango = db.query(RangoExperiencia).filter(
        RangoExperiencia.id_rango_experiencia == rango_experiencia_id
    ).first()

    if not rango:
        raise HTTPException(status_code=404, detail="Rango de experiencia no encontrado")

    if rango_data.descripcion_rango:
        rango.descripcion_rango = rango_data.descripcion_rango

    db.commit()
    db.refresh(rango)
    return rango


def delete_rango_experiencia(db: Session, rango_experiencia_id: int):
    """
    Elimina un rango de experiencia por su ID.

    Args:
        db (Session): Sesión activa de la base de datos.
        rango_experiencia_id (int): ID del rango.

    Returns:
        dict: Mensaje de confirmación.

    Raises:
        HTTPException: Si no se encuentra el rango.
    """
    rango = db.query(RangoExperiencia).filter(
        RangoExperiencia.id_rango_experiencia == rango_experiencia_id
    ).first()

    if not rango:
        raise HTTPException(status_code=404, detail="Rango de experiencia no encontrado")

    db.delete(rango)
    db.commit()
    return {"message": "Rango de experiencia eliminado correctamente"}
