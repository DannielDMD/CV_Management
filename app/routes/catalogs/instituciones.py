"""Rutas para la gestión del catálogo de instituciones académicas."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.schemas.catalogs.instituciones import (
    InstitucionAcademicaCreate,
    InstitucionAcademicaPaginatedResponse,
    InstitucionAcademicaUpdate,
    InstitucionAcademicaResponse,
)
from app.services.catalogs.instituciones_service import (
    get_institucion,
    get_instituciones,
    create_institucion,
    get_instituciones_academicas_con_paginacion,
    update_institucion,
    delete_institucion,
)

router = APIRouter(prefix="/instituciones", tags=["Instituciones Académicas"])


@router.get("/", response_model=InstitucionAcademicaPaginatedResponse)
def listar_instituciones_academicas_con_paginacion(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """
    Lista Instituciones academicas con búsqueda por nombre y paginación.
    """
    return get_instituciones_academicas_con_paginacion(
        db=db, skip=skip, limit=limit, search=search
    )


@router.get("/{institucion_id}", response_model=InstitucionAcademicaResponse)
def read_institucion(institucion_id: int, db: Session = Depends(get_db)):
    """
    Obtiene una institución académica por su ID.

    Args:
        institucion_id (int): ID de la institución.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        InstitucionAcademicaResponse: Institución encontrada.
    """
    return get_institucion(db, institucion_id)


@router.post("/", response_model=InstitucionAcademicaResponse, status_code=201)
def create_institucion_endpoint(
    institucion: InstitucionAcademicaCreate, db: Session = Depends(get_db)
):
    """
    Crea una nueva institución académica.

    Args:
        institucion (InstitucionAcademicaCreate): Datos de la nueva institución.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        InstitucionAcademicaResponse: Institución creada.
    """
    return create_institucion(db, institucion)


@router.put("/{institucion_id}", response_model=InstitucionAcademicaResponse)
def update_institucion_endpoint(
    institucion_id: int,
    institucion_update: InstitucionAcademicaUpdate,
    db: Session = Depends(get_db),
):
    """
    Actualiza una institución académica existente.

    Args:
        institucion_id (int): ID de la institución a actualizar.
        institucion_update (InstitucionAcademicaUpdate): Nuevos datos.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        InstitucionAcademicaResponse: Institución actualizada.
    """
    return update_institucion(db, institucion_id, institucion_update)


@router.delete("/{institucion_id}")
def delete_institucion_endpoint(institucion_id: int, db: Session = Depends(get_db)):
    """
    Elimina una institución académica por su ID.

    Args:
        institucion_id (int): ID de la institución a eliminar.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        dict: Mensaje de confirmación.
    """
    return delete_institucion(db, institucion_id)
