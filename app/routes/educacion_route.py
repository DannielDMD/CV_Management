"""Rutas para la gestión del historial educativo de los candidatos."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.services.educacion_service import (
    create_educacion,
    get_educacion_by_id,
    get_all_educaciones,
    get_educaciones_by_candidato,
    update_educacion,
    delete_educacion
)
from app.schemas.educacion_schema import (
    EducacionCreate,
    EducacionUpdate,
    EducacionResponse
)

router = APIRouter(prefix="/educaciones", tags=["Educaciones"])


@router.post("/", response_model=EducacionResponse)
def create_education(educacion_data: EducacionCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo registro educativo para un candidato.

    Args:
        educacion_data (EducacionCreate): Datos del registro educativo.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        EducacionResponse: Registro creado.
    """
    return create_educacion(db, educacion_data)


@router.get("/{id}", response_model=EducacionResponse)
def get_education(id: int, db: Session = Depends(get_db)):
    """
    Obtiene un registro educativo por su ID.

    Args:
        id (int): ID del registro educativo.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        EducacionResponse: Registro encontrado.
    """
    return get_educacion_by_id(db, id)


@router.get("/educaciones/candidato/{id_candidato}", response_model=List[EducacionResponse])
def obtener_educaciones_por_candidato(id_candidato: int, db: Session = Depends(get_db)):
    """
    Obtiene todos los registros educativos asociados a un candidato.

    Args:
        id_candidato (int): ID del candidato.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        List[EducacionResponse]: Lista de registros educativos del candidato.
    """
    return get_educaciones_by_candidato(db, id_candidato)


@router.get("/", response_model=List[EducacionResponse])
def get_all_educations(db: Session = Depends(get_db)):
    """
    Lista todos los registros educativos del sistema.

    Args:
        db (Session): Sesión de base de datos inyectada.

    Returns:
        List[EducacionResponse]: Lista de todos los registros.
    """
    return get_all_educaciones(db)


@router.put("/{id}", response_model=EducacionResponse)
def update_education(id: int, educacion_data: EducacionUpdate, db: Session = Depends(get_db)):
    """
    Actualiza un registro educativo existente.

    Args:
        id (int): ID del registro a actualizar.
        educacion_data (EducacionUpdate): Nuevos datos del registro.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        EducacionResponse: Registro actualizado.
    """
    return update_educacion(db, id, educacion_data)


@router.delete("/{id}")
def delete_education(id: int, db: Session = Depends(get_db)):
    """
    Elimina un registro educativo por su ID.

    Args:
        id (int): ID del registro educativo.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        dict: Resultado de la operación.
    """
    return delete_educacion(db, id)
