"""
Servicios para la gestión del catálogo de ciudades.
Incluye operaciones CRUD con validaciones de duplicados y existencia.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.catalogs.ciudad import Ciudad
from app.schemas.catalogs.ciudad import CiudadCreate
from app.utils.orden_catalogos import ordenar_por_nombre


def get_ciudades(db: Session):
    """
    Obtiene todas las ciudades ordenadas alfabéticamente por nombre.

    Args:
        db (Session): Sesión activa de la base de datos.

    Returns:
        List[Ciudad]: Lista de ciudades ordenadas.
    """
    query = db.query(Ciudad)
    return ordenar_por_nombre(query, "nombre_ciudad").all()


def get_ciudad_by_id(db: Session, ciudad_id: int):
    """
    Obtiene una ciudad por su ID.

    Args:
        db (Session): Sesión activa de la base de datos.
        ciudad_id (int): ID de la ciudad.

    Returns:
        Ciudad: Objeto Ciudad correspondiente.

    Raises:
        HTTPException: Si la ciudad no existe.
    """
    ciudad = db.query(Ciudad).filter(Ciudad.id_ciudad == ciudad_id).first()
    if not ciudad:
        raise HTTPException(status_code=404, detail="Ciudad no encontrada")
    return ciudad


def create_ciudad(db: Session, ciudad_data: CiudadCreate):
    """
    Crea una nueva ciudad si no existe previamente.

    Args:
        db (Session): Sesión activa de la base de datos.
        ciudad_data (CiudadCreate): Datos de la ciudad.

    Returns:
        Ciudad: Objeto ciudad creado.

    Raises:
        HTTPException: Si ya existe una ciudad con el mismo nombre.
    """
    existing_ciudad = db.query(Ciudad).filter(
        Ciudad.nombre_ciudad == ciudad_data.nombre_ciudad
    ).first()
    if existing_ciudad:
        raise HTTPException(status_code=400, detail="La ciudad ya existe")

    nueva_ciudad = Ciudad(nombre_ciudad=ciudad_data.nombre_ciudad)
    db.add(nueva_ciudad)
    db.commit()
    db.refresh(nueva_ciudad)
    return nueva_ciudad


def delete_ciudad(db: Session, ciudad_id: int):
    """
    Elimina una ciudad por su ID.

    Args:
        db (Session): Sesión activa de la base de datos.
        ciudad_id (int): ID de la ciudad a eliminar.

    Returns:
        dict: Mensaje de confirmación.

    Raises:
        HTTPException: Si la ciudad no existe.
    """
    ciudad = db.query(Ciudad).filter(Ciudad.id_ciudad == ciudad_id).first()
    if not ciudad:
        raise HTTPException(status_code=404, detail="Ciudad no encontrada")

    db.delete(ciudad)
    db.commit()
    return {"detail": "Ciudad eliminada correctamente"}
