"""Rutas para la gestión de cargos ofrecidos."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.catalogs.cargo_ofrecido import CargoOfrecidoCreate, CargoOfrecidoResponse
from app.services.catalogs.cargos_ofrecidos_service import (
    crear_cargo_ofrecido,
    obtener_cargos_ofrecidos,
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

@router.get("/", response_model=List[CargoOfrecidoResponse])
def listar_cargos(db: Session = Depends(get_db)):
    """
    Lista todos los cargos ofrecidos disponibles.

    Args:
        db (Session): Sesión de base de datos inyectada.

    Returns:
        List[CargoOfrecidoResponse]: Lista de cargos.
    """
    return obtener_cargos_ofrecidos(db)

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
