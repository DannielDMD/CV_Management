"""Rutas para la gestión de experiencias laborales de los candidatos."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.services.experiencia_service import (
    create_experiencia,
    get_experiencia_by_id,
    get_all_experiencias,
    get_experiencias_by_candidato,
    update_experiencia,
    delete_experiencia
)
from app.schemas.experiencia_schema import (
    ExperienciaLaboralCreate,
    ExperienciaLaboralUpdate,
    ExperienciaLaboralResponse
)

router = APIRouter(prefix="/experiencias", tags=["Experiencias Laborales"])


@router.post("/", response_model=ExperienciaLaboralResponse)
def create_experience(experiencia_data: ExperienciaLaboralCreate, db: Session = Depends(get_db)):
    """
    Crea una nueva experiencia laboral para un candidato.

    Args:
        experiencia_data (ExperienciaLaboralCreate): Datos de la experiencia.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        ExperienciaLaboralResponse: Experiencia registrada.
    """
    return create_experiencia(db, experiencia_data)


@router.get("/{id}", response_model=ExperienciaLaboralResponse)
def get_experience(id: int, db: Session = Depends(get_db)):
    """
    Obtiene una experiencia laboral por su ID.

    Args:
        id (int): ID de la experiencia.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        ExperienciaLaboralResponse: Datos de la experiencia encontrada.
    """
    return get_experiencia_by_id(db, id)


@router.get("/", response_model=List[ExperienciaLaboralResponse])
def get_all_experiences(db: Session = Depends(get_db)):
    """
    Lista todas las experiencias laborales registradas.

    Args:
        db (Session): Sesión de base de datos inyectada.

    Returns:
        List[ExperienciaLaboralResponse]: Lista completa de experiencias.
    """
    return get_all_experiencias(db)


@router.put("/{id}", response_model=ExperienciaLaboralResponse)
def update_experience(id: int, experiencia_data: ExperienciaLaboralUpdate, db: Session = Depends(get_db)):
    """
    Actualiza una experiencia laboral existente.

    Args:
        id (int): ID de la experiencia a actualizar.
        experiencia_data (ExperienciaLaboralUpdate): Nuevos datos de la experiencia.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        ExperienciaLaboralResponse: Experiencia actualizada.
    """
    return update_experiencia(db, id, experiencia_data)


@router.get("/candidato/{id_candidato}", response_model=List[ExperienciaLaboralResponse])
def get_experiences_by_candidate(id_candidato: int, db: Session = Depends(get_db)):
    """
    Obtiene todas las experiencias laborales de un candidato específico.

    Args:
        id_candidato (int): ID del candidato.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        List[ExperienciaLaboralResponse]: Lista de experiencias del candidato.
    """
    return get_experiencias_by_candidato(db, id_candidato)


@router.delete("/{id}")
def delete_experience(id: int, db: Session = Depends(get_db)):
    """
    Elimina una experiencia laboral por su ID.

    Args:
        id (int): ID de la experiencia a eliminar.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        dict: Resultado de la operación.
    """
    return delete_experiencia(db, id)
