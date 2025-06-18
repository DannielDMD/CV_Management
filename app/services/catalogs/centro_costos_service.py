"""Servicios para la gestión del catálogo de centros de costos."""

import math
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional

from app.models.catalogs.centro_costos import CentroCostos
from app.schemas.catalogs.centro_costos import CentroCostosCreate, CentroCostosPaginatedResponse
from app.utils.orden_catalogos import ordenar_por_nombre


def get_centros_costos(db: Session) -> List[CentroCostos]:
    """
    Obtiene todos los centros de costos ordenados alfabéticamente.
    """
    query = db.query(CentroCostos)
    return ordenar_por_nombre(query, "nombre_centro_costos").all()


def get_centro_costos_by_id(db: Session, id_centro: int) -> Optional[CentroCostos]:
    """
    Busca un centro de costos por su ID.
    """
    return db.query(CentroCostos).filter(CentroCostos.id_centro_costos == id_centro).first()



def get_centros_costos_con_paginacion(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None
) -> CentroCostosPaginatedResponse:
    """
    Retorna centros de costos con búsqueda y paginación.
    """
    query = db.query(CentroCostos)

    if search:
        query = query.filter(CentroCostos.nombre_centro_costos.ilike(f"%{search}%"))

    total = query.count()

    resultados = query.order_by(CentroCostos.nombre_centro_costos.asc())\
        .offset(skip).limit(limit).all()

    page = (skip // limit) + 1 if limit > 0 else 1
    total_pages = math.ceil(total / limit) if limit > 0 else 1

    return CentroCostosPaginatedResponse(
        total=total,
        page=page,
        per_page=limit,
        total_pages=total_pages,
        resultados=resultados
    )



def create_centro_costos(db: Session, data: CentroCostosCreate) -> Optional[CentroCostos]:
    """
    Crea un nuevo centro de costos si no existe uno con el mismo nombre.
    """
    nombre = data.nombre_centro_costos.strip()
    existente = db.query(CentroCostos).filter(CentroCostos.nombre_centro_costos.ilike(nombre)).first()
    if existente:
        return None

    nuevo = CentroCostos(nombre_centro_costos=nombre)
    db.add(nuevo)
    try:
        db.commit()
        db.refresh(nuevo)
        return nuevo
    except IntegrityError:
        db.rollback()
        return None


def update_centro_costos(db: Session, id_centro: int, data: CentroCostosCreate) -> Optional[CentroCostos]:
    """
    Actualiza el nombre de un centro de costos si no hay duplicados.
    """
    centro = get_centro_costos_by_id(db, id_centro)
    if not centro:
        return None

    nuevo_nombre = data.nombre_centro_costos.strip()
    duplicado = db.query(CentroCostos).filter(
        CentroCostos.nombre_centro_costos.ilike(nuevo_nombre),
        CentroCostos.id_centro_costos != id_centro
    ).first()
    if duplicado:
        return None

    centro.nombre_centro_costos = nuevo_nombre
    try:
        db.commit()
        db.refresh(centro)
        return centro
    except IntegrityError:
        db.rollback()
        return None


def delete_centro_costos(db: Session, id_centro: int) -> bool:
    """
    Elimina un centro de costos si existe.
    """
    centro = get_centro_costos_by_id(db, id_centro)
    if not centro:
        return False
    try:
        db.delete(centro)
        db.commit()
        return True
    except IntegrityError:
        db.rollback()
        return False
