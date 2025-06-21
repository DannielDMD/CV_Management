"""Rutas para la gestión del catálogo de disponibilidades laborales."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from typing import List, Optional

from app.core.database import get_db
from app.services.catalogs.disponibilidad_service import (
    get_all_disponibilidades,
    get_disponabilidad_con_paginacion,
    get_disponibilidad,
    create_disponibilidad,
    update_disponibilidad,
    delete_disponibilidad,
)
from app.schemas.preferencias_schema import (
    DisponibilidadCreate,
    DisponibilidadPaginatedResponse,
    DisponibilidadUpdate,
    DisponibilidadResponse,
)

router = APIRouter(prefix="/disponibilidades", tags=["Disponibilidad"])



@router.get("/todas", response_model=List[DisponibilidadResponse])
def listar_disponibilidades(db: Session = Depends(get_db)):
    return get_all_disponibilidades(db)

@router.get("/", response_model=DisponibilidadPaginatedResponse)
def listar_disponabilidad_con_paginacion(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """
    Lista Disponibilidades con búsqueda por nombre y paginación.
    """
    return get_disponabilidad_con_paginacion(
        db=db, skip=skip, limit=limit, search=search
    )



@router.get("/{disponibilidad_id}", response_model=DisponibilidadResponse)
def obtener_disponibilidad(disponibilidad_id: int, db: Session = Depends(get_db)):
    """
    Obtiene una disponibilidad específica por su ID.

    Args:
        disponibilidad_id (int): ID del registro.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        DisponibilidadResponse: Registro encontrado.

    Raises:
        HTTPException: Si no se encuentra el registro.
    """
    try:
        return get_disponibilidad(db, disponibilidad_id)
    except NoResultFound:
        raise HTTPException(
            status_code=404,
            detail=f"Disponibilidad con ID {disponibilidad_id} no encontrada",
        )


@router.post("/", response_model=DisponibilidadResponse)
def crear_disponibilidad(disponibilidad_data: DisponibilidadCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo registro de disponibilidad.

    Args:
        disponibilidad_data (DisponibilidadCreate): Datos del nuevo registro.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        DisponibilidadResponse: Registro creado.

    Raises:
        HTTPException: Si ocurre un error de validación.
    """
    try:
        return create_disponibilidad(db, disponibilidad_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{disponibilidad_id}", response_model=DisponibilidadResponse)
def actualizar_disponibilidad(
    disponibilidad_id: int,
    disponibilidad_data: DisponibilidadUpdate,
    db: Session = Depends(get_db),
):
    """
    Actualiza un registro de disponibilidad existente.

    Args:
        disponibilidad_id (int): ID del registro a actualizar.
        disponibilidad_data (DisponibilidadUpdate): Nuevos datos.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        DisponibilidadResponse: Registro actualizado.

    Raises:
        HTTPException: Si el registro no se encuentra.
    """
    try:
        return update_disponibilidad(db, disponibilidad_id, disponibilidad_data)
    except NoResultFound:
        raise HTTPException(
            status_code=404,
            detail=f"Disponibilidad con ID {disponibilidad_id} no encontrada",
        )


@router.delete("/{disponibilidad_id}")
def eliminar_disponibilidad(disponibilidad_id: int, db: Session = Depends(get_db)):
    """
    Elimina un registro de disponibilidad por su ID.

    Args:
        disponibilidad_id (int): ID del registro a eliminar.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        dict: Mensaje de confirmación.

    Raises:
        HTTPException: Si el registro no se encuentra.
    """
    try:
        return delete_disponibilidad(db, disponibilidad_id)
    except NoResultFound:
        raise HTTPException(
            status_code=404,
            detail=f"Disponibilidad con ID {disponibilidad_id} no encontrada",
        )
