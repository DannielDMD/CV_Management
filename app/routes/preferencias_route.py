"""Rutas para la gestión de preferencias laborales de los candidatos."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.preferencias_service import (
    obtener_preferencia_candidato,
    crear_preferencia,
    actualizar_preferencia,
    eliminar_preferencia
)
from app.schemas.preferencias_schema import (
    PreferenciaDisponibilidadCreate,
    PreferenciaDisponibilidadUpdate,
    PreferenciaDisponibilidadResponse
)

router = APIRouter(prefix="/preferencias", tags=["Preferencias"])


@router.get("/{id_candidato}", response_model=PreferenciaDisponibilidadResponse)
def get_preferencia(id_candidato: int, db: Session = Depends(get_db)):
    """
    Obtiene la preferencia y disponibilidad de un candidato por su ID.

    Args:
        id_candidato (int): ID del candidato.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        PreferenciaDisponibilidadResponse: Datos de preferencias del candidato.
    """
    return obtener_preferencia_candidato(db, id_candidato)


@router.post("/", response_model=PreferenciaDisponibilidadResponse)
def create_preferencia(preferencia_data: PreferenciaDisponibilidadCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo registro de preferencias y disponibilidad para un candidato.

    Args:
        preferencia_data (PreferenciaDisponibilidadCreate): Datos de la nueva preferencia.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        PreferenciaDisponibilidadResponse: Registro creado.
    """
    return crear_preferencia(db, preferencia_data)


@router.put("/{id_candidato}", response_model=PreferenciaDisponibilidadResponse)
def update_preferencia(id_candidato: int, preferencia_data: PreferenciaDisponibilidadUpdate, db: Session = Depends(get_db)):
    """
    Actualiza las preferencias de un candidato.

    Args:
        id_candidato (int): ID del candidato.
        preferencia_data (PreferenciaDisponibilidadUpdate): Nuevos datos de preferencia.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        PreferenciaDisponibilidadResponse: Registro actualizado.
    """
    return actualizar_preferencia(db, id_candidato, preferencia_data)


@router.delete("/{id_candidato}")
def delete_preferencia(id_candidato: int, db: Session = Depends(get_db)):
    """
    Elimina el registro de preferencias de un candidato por su ID.

    Args:
        id_candidato (int): ID del candidato.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        dict: Resultado de la operación.
    """
    return eliminar_preferencia(db, id_candidato)
