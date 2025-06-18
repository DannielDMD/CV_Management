"""Rutas para la gestión del catálogo de rangos de experiencia laboral."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.schemas.catalogs.rango_experiencia import (
    RangoExperienciaPaginatedResponse,
    RangoExperienciaResponse,
    RangoExperienciaCreate,
    RangoExperienciaUpdate
)
from app.services.catalogs.rango_experiencia_service import (
    get_rango_experiencia_con_paginacion,
    get_rangos_experiencia,
    get_rango_experiencia,
    create_rango_experiencia,
    update_rango_experiencia,
    delete_rango_experiencia
)

router = APIRouter(prefix="/rangos-experiencia", tags=["Rangos de Experiencia"])


@router.get("/", response_model=RangoExperienciaPaginatedResponse)
def listar_rango_experiencia_con_paginacion(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """
    Lista Rangos de Experiencia con búsqueda por nombre y paginación.
    """
    return get_rango_experiencia_con_paginacion(db=db, skip=skip, limit=limit, search=search)



@router.get("/{rango_experiencia_id}", response_model=RangoExperienciaResponse)
def obtener_rango_experiencia(rango_experiencia_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un rango de experiencia por su ID.

    Args:
        rango_experiencia_id (int): ID del rango a consultar.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        RangoExperienciaResponse: Rango encontrado.
    """
    return get_rango_experiencia(db, rango_experiencia_id)


@router.post("/", response_model=RangoExperienciaResponse)
def crear_rango_experiencia(rango_data: RangoExperienciaCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo rango de experiencia.

    Args:
        rango_data (RangoExperienciaCreate): Datos del nuevo rango.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        RangoExperienciaResponse: Rango creado.
    """
    return create_rango_experiencia(db, rango_data)


@router.put("/{rango_experiencia_id}", response_model=RangoExperienciaResponse)
def actualizar_rango_experiencia(
    rango_experiencia_id: int,
    rango_data: RangoExperienciaUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualiza un rango de experiencia existente.

    Args:
        rango_experiencia_id (int): ID del rango a actualizar.
        rango_data (RangoExperienciaUpdate): Nuevos datos del rango.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        RangoExperienciaResponse: Rango actualizado.
    """
    return update_rango_experiencia(db, rango_experiencia_id, rango_data)


@router.delete("/{rango_experiencia_id}")
def eliminar_rango_experiencia(rango_experiencia_id: int, db: Session = Depends(get_db)):
    """
    Elimina un rango de experiencia por su ID.

    Args:
        rango_experiencia_id (int): ID del rango a eliminar.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        dict: Mensaje de confirmación.
    """
    return delete_rango_experiencia(db, rango_experiencia_id)
