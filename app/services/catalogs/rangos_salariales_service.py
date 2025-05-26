"""
Servicios para el catálogo de Rangos Salariales.
Incluye funciones CRUD: listar, obtener, crear, actualizar y eliminar.
"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, NoResultFound
from fastapi import HTTPException
from app.models.preferencias import RangoSalarial
from app.schemas.preferencias_schema import RangoSalarialCreate, RangoSalarialUpdate


def get_all_rangos_salariales(db: Session):
    """
    Obtiene todos los rangos salariales registrados.

    Args:
        db (Session): Sesión activa de la base de datos.

    Returns:
        List[RangoSalarial]: Lista de rangos salariales.
    """
    return db.query(RangoSalarial).all()


def get_rango_salarial(db: Session, rango_id: int):
    """
    Obtiene un rango salarial por su ID.

    Args:
        db (Session): Sesión activa de la base de datos.
        rango_id (int): ID del rango.

    Returns:
        RangoSalarial: Objeto encontrado.

    Raises:
        NoResultFound: Si no existe un rango con el ID dado.
    """
    rango = db.query(RangoSalarial).filter(
        RangoSalarial.id_rango_salarial == rango_id
    ).first()

    if not rango:
        raise NoResultFound(f"Rango Salarial con ID {rango_id} no encontrado")

    return rango


def create_rango_salarial(db: Session, rango_data: RangoSalarialCreate):
    """
    Crea un nuevo rango salarial si no existe uno con la misma descripción.

    Args:
        db (Session): Sesión activa de la base de datos.
        rango_data (RangoSalarialCreate): Datos del nuevo rango.

    Returns:
        RangoSalarial: Objeto creado.

    Raises:
        ValueError: Si ya existe una descripción duplicada.
    """
    try:
        nuevo_rango = RangoSalarial(descripcion_rango=rango_data.descripcion_rango)
        db.add(nuevo_rango)
        db.commit()
        db.refresh(nuevo_rango)
        return nuevo_rango
    except IntegrityError:
        db.rollback()
        raise ValueError("Ya existe un Rango Salarial con esa descripción")


def update_rango_salarial(db: Session, rango_id: int, rango_data: RangoSalarialUpdate):
    """
    Actualiza un rango salarial por ID.

    Args:
        db (Session): Sesión activa de la base de datos.
        rango_id (int): ID del rango a actualizar.
        rango_data (RangoSalarialUpdate): Datos a modificar.

    Returns:
        RangoSalarial: Objeto actualizado.
    """
    rango = get_rango_salarial(db, rango_id)

    if rango_data.descripcion_rango:
        rango.descripcion_rango = rango_data.descripcion_rango

    db.commit()
    db.refresh(rango)
    return rango


def delete_rango_salarial(db: Session, rango_id: int):
    """
    Elimina un rango salarial por su ID.

    Args:
        db (Session): Sesión activa de la base de datos.
        rango_id (int): ID del rango a eliminar.

    Returns:
        dict: Mensaje de éxito.
    """
    rango = get_rango_salarial(db, rango_id)
    db.delete(rango)
    db.commit()
    return {"message": f"Rango Salarial con ID {rango_id} eliminado correctamente"}
