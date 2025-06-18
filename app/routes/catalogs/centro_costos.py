"""Rutas para la gestión del catálogo de centros de costos."""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.catalogs.centro_costos import CentroCostosCreate, CentroCostosPaginatedResponse, CentroCostosResponse
from app.services.catalogs.centro_costos_service import (
    get_centros_costos,
    get_centro_costos_by_id,
    create_centro_costos,
    get_centros_costos_con_paginacion,
    update_centro_costos,
    delete_centro_costos,
)

router = APIRouter(prefix="/centros-costos", tags=["Centros de Costos"])


@router.get("/", response_model=CentroCostosPaginatedResponse)
def listar_centros_costos_con_paginacion(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Lista de centros de costos con búsqueda por nombre y paginación.
    """
    return get_centros_costos_con_paginacion(
        db=db,
        skip=skip,
        limit=limit,
        search=search
    )


@router.get("/{id_centro}", response_model=CentroCostosResponse)
def obtener_centro_costos(id_centro: int, db: Session = Depends(get_db)):
    centro = get_centro_costos_by_id(db, id_centro)
    if not centro:
        raise HTTPException(status_code=404, detail="Centro de costos no encontrado")
    return centro


@router.post("/", response_model=CentroCostosResponse, status_code=status.HTTP_201_CREATED)
def crear_centro_costos(data: CentroCostosCreate, db: Session = Depends(get_db)):
    nuevo = create_centro_costos(db, data)
    if not nuevo:
        raise HTTPException(status_code=400, detail="Ya existe un centro de costos con ese nombre")
    return nuevo


@router.put("/{id_centro}", response_model=CentroCostosResponse)
def actualizar_centro_costos(id_centro: int, data: CentroCostosCreate, db: Session = Depends(get_db)):
    actualizado = update_centro_costos(db, id_centro, data)
    if not actualizado:
        raise HTTPException(status_code=400, detail="No se pudo actualizar (posible duplicado o no encontrado)")
    return actualizado


@router.delete("/{id_centro}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_centro_costos(id_centro: int, db: Session = Depends(get_db)):
    eliminado = delete_centro_costos(db, id_centro)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Centro de costos no encontrado o no se pudo eliminar")
