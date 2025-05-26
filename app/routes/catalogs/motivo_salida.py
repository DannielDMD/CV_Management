"""Rutas para la gestión del catálogo de motivos de salida laboral."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.catalogs.motivo_salida import (
    MotivoSalidaCreate,
    MotivoSalidaUpdate,
    MotivoSalidaResponse,
)
from app.services.catalogs.motivo_salida_service import (
    get_motivos_salida,
    get_motivo_salida,
    create_motivo_salida,
    update_motivo_salida,
    delete_motivo_salida,
)

router = APIRouter(prefix="/motivos-salida", tags=["Motivos de Salida"])


@router.get("/", response_model=List[MotivoSalidaResponse])
def obtener_motivos_salida(db: Session = Depends(get_db)):
    """
    Lista todos los motivos de salida registrados.

    Args:
        db (Session): Sesión de base de datos inyectada.

    Returns:
        List[MotivoSalidaResponse]: Lista de motivos.
    """
    return get_motivos_salida(db)


@router.get("/{id_motivo_salida}", response_model=MotivoSalidaResponse)
def obtener_motivo_salida(id_motivo_salida: int, db: Session = Depends(get_db)):
    """
    Obtiene un motivo de salida por su ID.

    Args:
        id_motivo_salida (int): ID del motivo.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        MotivoSalidaResponse: Motivo encontrado.

    Raises:
        HTTPException: Si el motivo no existe.
    """
    motivo = get_motivo_salida(db, id_motivo_salida)
    if not motivo:
        raise HTTPException(status_code=404, detail="Motivo de salida no encontrado")
    return motivo


@router.post("/", response_model=MotivoSalidaResponse, status_code=201)
def crear_motivo_salida(motivo_data: MotivoSalidaCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo motivo de salida.

    Args:
        motivo_data (MotivoSalidaCreate): Datos del nuevo motivo.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        MotivoSalidaResponse: Motivo creado.
    """
    return create_motivo_salida(db, motivo_data)


@router.put("/{id_motivo_salida}", response_model=MotivoSalidaResponse)
def actualizar_motivo_salida(
    id_motivo_salida: int,
    motivo_data: MotivoSalidaUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualiza un motivo de salida existente.

    Args:
        id_motivo_salida (int): ID del motivo a actualizar.
        motivo_data (MotivoSalidaUpdate): Nuevos datos.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        MotivoSalidaResponse: Motivo actualizado.

    Raises:
        HTTPException: Si el motivo no existe.
    """
    motivo_actualizado = update_motivo_salida(db, id_motivo_salida, motivo_data)
    if not motivo_actualizado:
        raise HTTPException(status_code=404, detail="Motivo de salida no encontrado")
    return motivo_actualizado


@router.delete("/{id_motivo_salida}", status_code=204)
def eliminar_motivo_salida(id_motivo_salida: int, db: Session = Depends(get_db)):
    """
    Elimina un motivo de salida por su ID.

    Args:
        id_motivo_salida (int): ID del motivo a eliminar.
        db (Session): Sesión de base de datos inyectada.

    Raises:
        HTTPException: Si el motivo no existe.
    """
    if not delete_motivo_salida(db, id_motivo_salida):
        raise HTTPException(status_code=404, detail="Motivo de salida no encontrado")
