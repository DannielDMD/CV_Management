"""Rutas para la gestión del catálogo de ciudades."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.catalogs.ciudad import CiudadCreate, CiudadResponse
from app.services.catalogs.ciudades_service import (
    get_ciudades,   
    get_ciudad_by_id,
    create_ciudad,
    delete_ciudad,
)

router = APIRouter(
    prefix="/ciudades",
    tags=["Ciudades"]
)

@router.get("/", response_model=List[CiudadResponse])
def obtener_ciudades(db: Session = Depends(get_db)):
    """
    Obtiene todas las ciudades registradas.

    Args:
        db (Session): Sesión de base de datos inyectada.

    Returns:
        List[CiudadResponse]: Lista de ciudades.
    """
    return get_ciudades(db)

@router.get("/{ciudad_id}", response_model=CiudadResponse)
def obtener_ciudad(ciudad_id: int, db: Session = Depends(get_db)):
    """
    Obtiene una ciudad específica por su ID.

    Args:
        ciudad_id (int): ID de la ciudad.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        CiudadResponse: Ciudad encontrada.
    """
    return get_ciudad_by_id(db, ciudad_id)

@router.post("/", response_model=CiudadResponse, status_code=201)
def crear_ciudad(ciudad: CiudadCreate, db: Session = Depends(get_db)):
    """
    Crea una nueva ciudad en el catálogo.

    Args:
        ciudad (CiudadCreate): Datos de la nueva ciudad.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        CiudadResponse: Ciudad creada.
    """
    return create_ciudad(db, ciudad)

@router.delete("/{ciudad_id}")
def eliminar_ciudad(ciudad_id: int, db: Session = Depends(get_db)):
    """
    Elimina una ciudad del catálogo por su ID.

    Args:
        ciudad_id (int): ID de la ciudad a eliminar.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        dict: Mensaje de confirmación.
    """
    return delete_ciudad(db, ciudad_id)
