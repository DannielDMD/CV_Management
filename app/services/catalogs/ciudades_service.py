"""
Servicios para la gestión del catálogo de ciudades.
Incluye operaciones CRUD con validaciones de duplicados y existencia.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.catalogs.ciudad import Ciudad
from app.schemas.catalogs.ciudad import CiudadCreate
from app.utils.orden_catalogos import ordenar_por_nombre


def get_ciudades(db: Session) -> List[Ciudad]:
    """
    Obtiene todas las ciudades ordenadas alfabéticamente.
    """
    query = db.query(Ciudad)
    return ordenar_por_nombre(query, "nombre_ciudad").all()


def get_ciudad_by_id(db: Session, ciudad_id: int) -> Optional[Ciudad]:
    """
    Busca una ciudad por su ID.
    """
    return db.query(Ciudad).filter(Ciudad.id_ciudad == ciudad_id).first()


def get_ciudades_por_departamento(db: Session, id_departamento: int) -> List[Ciudad]:
    """
    Obtiene ciudades asociadas a un departamento específico.
    """
    return db.query(Ciudad).filter(Ciudad.id_departamento == id_departamento).order_by(Ciudad.nombre_ciudad.asc()).all()


def create_ciudad(db: Session, ciudad_data: CiudadCreate) -> Optional[Ciudad]:
    """
    Crea una ciudad si no existe una con el mismo nombre dentro del mismo departamento.
    """
    existente = db.query(Ciudad).filter(
        Ciudad.nombre_ciudad.ilike(ciudad_data.nombre_ciudad.strip()),
        Ciudad.id_departamento == ciudad_data.id_departamento
    ).first()
    if existente:
        return None

    nueva_ciudad = Ciudad(
        nombre_ciudad=ciudad_data.nombre_ciudad.strip(),
        id_departamento=ciudad_data.id_departamento
    )
    db.add(nueva_ciudad)
    try:
        db.commit()
        db.refresh(nueva_ciudad)
        return nueva_ciudad
    except IntegrityError:
        db.rollback()
        return None


def delete_ciudad(db: Session, ciudad_id: int) -> bool:
    """
    Elimina una ciudad por ID.
    """
    ciudad = get_ciudad_by_id(db, ciudad_id)
    if not ciudad:
        return False
    try:
        db.delete(ciudad)
        db.commit()
        return True
    except IntegrityError:
        db.rollback()
        return False
