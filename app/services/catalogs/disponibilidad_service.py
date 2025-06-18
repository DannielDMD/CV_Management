"""
Servicios para el catálogo de Disponibilidad.
Incluye operaciones CRUD con validaciones de duplicidad y existencia.
"""

import math
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, NoResultFound
from app.models.preferencias import Disponibilidad
from app.schemas.preferencias_schema import DisponibilidadCreate, DisponibilidadPaginatedResponse, DisponibilidadUpdate


def get_disponabilidad_con_paginacion(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None
) -> DisponibilidadPaginatedResponse:
    """
    Retorna Disponibilidades con búsqueda y paginación.
    """
    query = db.query(Disponibilidad)

    if search:
        query = query.filter(Disponibilidad.descripcion_disponibilidad.ilike(f"%{search}%"))

    total = query.count()

    resultados = query.order_by(Disponibilidad.descripcion_disponibilidad.asc())\
        .offset(skip).limit(limit).all()

    page = (skip // limit) + 1 if limit > 0 else 1
    total_pages = math.ceil(total / limit) if limit > 0 else 1

    return DisponibilidadPaginatedResponse(
        total=total,
        page=page,
        per_page=limit,
        total_pages=total_pages,
        resultados=resultados
    )


def get_disponibilidad(db: Session, disponibilidad_id: int):
    """
    Obtiene una disponibilidad por su ID.

    Args:
        db (Session): Sesión activa.
        disponibilidad_id (int): ID a buscar.

    Returns:
        Disponibilidad: Objeto disponibilidad encontrado.

    Raises:
        NoResultFound: Si el ID no existe en la base de datos.
    """
    disponibilidad = (
        db.query(Disponibilidad)
        .filter(Disponibilidad.id_disponibilidad == disponibilidad_id)
        .first()
    )
    if not disponibilidad:
        raise NoResultFound(f"Disponibilidad con ID {disponibilidad_id} no encontrada")
    return disponibilidad


def create_disponibilidad(db: Session, disponibilidad_data: DisponibilidadCreate):
    """
    Crea una nueva disponibilidad si no existe una igual.

    Args:
        db (Session): Sesión activa.
        disponibilidad_data (DisponibilidadCreate): Datos a registrar.

    Returns:
        Disponibilidad: Registro creado.

    Raises:
        ValueError: Si ya existe una disponibilidad con el mismo nombre.
    """
    try:
        nueva_disponibilidad = Disponibilidad(
            descripcion_disponibilidad=disponibilidad_data.descripcion_disponibilidad
        )
        db.add(nueva_disponibilidad)
        db.commit()
        db.refresh(nueva_disponibilidad)
        return nueva_disponibilidad
    except IntegrityError:
        db.rollback()
        raise ValueError("Ya existe una Disponibilidad con esa descripción")


def update_disponibilidad(db: Session, disponibilidad_id: int, disponibilidad_data: DisponibilidadUpdate):
    """
    Actualiza una disponibilidad por su ID.

    Args:
        db (Session): Sesión activa.
        disponibilidad_id (int): ID del registro a modificar.
        disponibilidad_data (DisponibilidadUpdate): Nuevos datos.

    Returns:
        Disponibilidad: Objeto actualizado.
    """
    disponibilidad = get_disponibilidad(db, disponibilidad_id)
    if disponibilidad_data.descripcion_disponibilidad:
        disponibilidad.descripcion_disponibilidad = disponibilidad_data.descripcion_disponibilidad
    db.commit()
    db.refresh(disponibilidad)
    return disponibilidad


def delete_disponibilidad(db: Session, disponibilidad_id: int):
    """
    Elimina una disponibilidad por su ID.

    Args:
        db (Session): Sesión activa.
        disponibilidad_id (int): ID a eliminar.

    Returns:
        dict: Mensaje de confirmación.
    """
    disponibilidad = get_disponibilidad(db, disponibilidad_id)
    db.delete(disponibilidad)
    db.commit()
    return {
        "message": f"Disponibilidad con ID {disponibilidad_id} eliminada correctamente"
    }
