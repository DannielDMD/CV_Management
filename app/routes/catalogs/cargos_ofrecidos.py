"""Rutas para la gestión de cargos ofrecidos."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.schemas.catalogs.cargo_ofrecido import (
    CargoOfrecidoCreate,
    CargoOfrecidoPaginatedResponse,
    CargoOfrecidoResponse,
)
from app.services.catalogs.cargos_ofrecidos_service import (
    crear_cargo_ofrecido,
    get_cargos_con_paginacion,
    obtener_cargos_ofrecidos, #Ver si eliminar
    obtener_cargo_ofrecido_por_id,
    eliminar_cargo_ofrecido,
)

router = APIRouter(prefix="/cargo-ofrecido", tags=["Cargo Ofrecido"])


@router.post("/", response_model=CargoOfrecidoResponse)
def crear_cargo(cargo_data: CargoOfrecidoCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo cargo ofrecido.

    Args:
        cargo_data (CargoOfrecidoCreate): Datos del nuevo cargo.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        CargoOfrecidoResponse: Cargo creado.
    """
    return crear_cargo_ofrecido(db, cargo_data)


@router.get("/", response_model=CargoOfrecidoPaginatedResponse)
def listar_cargos_ofrecidos_con_paginacion(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """
    Lista de cargos ofrecidos con paginación y búsqueda opcional por nombre.
    """
    return get_cargos_con_paginacion(db=db, skip=skip, limit=limit, search=search)


@router.get("/{id_cargo}", response_model=CargoOfrecidoResponse)
def obtener_cargo(id_cargo: int, db: Session = Depends(get_db)):
    """
    Obtiene un cargo ofrecido por su ID.

    Args:
        id_cargo (int): ID del cargo a consultar.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        CargoOfrecidoResponse: Cargo encontrado.
    """
    return obtener_cargo_ofrecido_por_id(db, id_cargo)


@router.delete("/{id_cargo}")
def eliminar_cargo(id_cargo: int, db: Session = Depends(get_db)):
    """
    Elimina un cargo ofrecido por su ID.

    Args:
        id_cargo (int): ID del cargo a eliminar.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        dict: Mensaje de confirmación.
    """
    return eliminar_cargo_ofrecido(db, id_cargo)
