"""Rutas para la gestión del catálogo de rangos salariales."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from typing import List, Optional

from app.core.database import get_db
from app.schemas.preferencias_schema import (
    RangoSalarialCreate,
    RangoSalarialPaginatedResponse,
    RangoSalarialUpdate,
    RangoSalarialResponse
)
from app.services.catalogs.rangos_salariales_service import (
    get_rango_salarial,
    create_rango_salarial,
    get_rango_salarial_con_paginacion,
    update_rango_salarial,
    delete_rango_salarial
)

router = APIRouter(prefix="/rangos-salariales", tags=["Rangos Salariales"])


@router.get("/", response_model=RangoSalarialPaginatedResponse)
def listar_rango_salarial_con_paginacion(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """
    Lista Rangos Salarial con búsqueda por nombre y paginación.
    """
    return get_rango_salarial_con_paginacion(db=db, skip=skip, limit=limit, search=search)




@router.get("/{rango_id}", response_model=RangoSalarialResponse)
def obtener_rango_salarial(rango_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un rango salarial por su ID.

    Args:
        rango_id (int): ID del rango a consultar.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        RangoSalarialResponse: Rango encontrado.

    Raises:
        HTTPException: Si el rango no existe.
    """
    try:
        return get_rango_salarial(db, rango_id)
    except NoResultFound:
        raise HTTPException(
            status_code=404,
            detail=f"Rango Salarial con ID {rango_id} no encontrado"
        )


@router.post("/", response_model=RangoSalarialResponse)
def crear_rango_salarial(rango_data: RangoSalarialCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo rango salarial.

    Args:
        rango_data (RangoSalarialCreate): Datos del nuevo rango.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        RangoSalarialResponse: Rango creado.

    Raises:
        HTTPException: Si ocurre un error de validación.
    """
    try:
        return create_rango_salarial(db, rango_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{rango_id}", response_model=RangoSalarialResponse)
def actualizar_rango_salarial(
    rango_id: int,
    rango_data: RangoSalarialUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualiza un rango salarial existente.

    Args:
        rango_id (int): ID del rango a actualizar.
        rango_data (RangoSalarialUpdate): Nuevos datos del rango.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        RangoSalarialResponse: Rango actualizado.

    Raises:
        HTTPException: Si el rango no existe.
    """
    try:
        return update_rango_salarial(db, rango_id, rango_data)
    except NoResultFound:
        raise HTTPException(
            status_code=404,
            detail=f"Rango Salarial con ID {rango_id} no encontrado"
        )


@router.delete("/{rango_id}")
def eliminar_rango_salarial(rango_id: int, db: Session = Depends(get_db)):
    """
    Elimina un rango salarial por su ID.

    Args:
        rango_id (int): ID del rango a eliminar.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        dict: Mensaje de confirmación.

    Raises:
        HTTPException: Si el rango no existe.
    """
    try:
        return delete_rango_salarial(db, rango_id)
    except NoResultFound:
        raise HTTPException(
            status_code=404,
            detail=f"Rango Salarial con ID {rango_id} no encontrado"
        )
