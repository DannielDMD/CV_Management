"""Rutas para la gestión del catálogo de niveles de educación."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.catalogs.nivel_educacion import (
    NivelEducacionCreate,
    NivelEducacionUpdate,
    NivelEducacionResponse
)
from app.services.catalogs.nivel_educacion_service import (
    get_niveles_educacion, 
    get_nivel_educacion, 
    create_nivel_educacion, 
    update_nivel_educacion, 
    delete_nivel_educacion
)

router = APIRouter(prefix="/nivel-educacion", tags=["Nivel Educación"])


@router.get("/", response_model=List[NivelEducacionResponse])
def listar_niveles_educacion(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Lista todos los niveles de educación registrados.

    Args:
        skip (int): Número de registros a omitir (paginación).
        limit (int): Número máximo de registros a retornar.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        List[NivelEducacionResponse]: Lista de niveles de educación.
    """
    return get_niveles_educacion(db, skip, limit)


@router.get("/{id_nivel_educacion}", response_model=NivelEducacionResponse)
def obtener_nivel_educacion(id_nivel_educacion: int, db: Session = Depends(get_db)):
    """
    Obtiene un nivel de educación por su ID.

    Args:
        id_nivel_educacion (int): ID del nivel de educación.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        NivelEducacionResponse: Nivel de educación encontrado.

    Raises:
        HTTPException: Si el registro no existe.
    """
    nivel = get_nivel_educacion(db, id_nivel_educacion)
    if not nivel:
        raise HTTPException(status_code=404, detail="Nivel de educación no encontrado")
    return nivel


@router.post("/", response_model=NivelEducacionResponse)
def crear_nivel_educacion(nivel_educacion_data: NivelEducacionCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo nivel de educación.

    Args:
        nivel_educacion_data (NivelEducacionCreate): Datos del nuevo nivel.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        NivelEducacionResponse: Nivel de educación creado.
    """
    return create_nivel_educacion(db, nivel_educacion_data)


@router.put("/{id_nivel_educacion}", response_model=NivelEducacionResponse)
def actualizar_nivel_educacion(
    id_nivel_educacion: int,
    nivel_educacion_data: NivelEducacionUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualiza un nivel de educación existente.

    Args:
        id_nivel_educacion (int): ID del nivel a actualizar.
        nivel_educacion_data (NivelEducacionUpdate): Nuevos datos del nivel.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        NivelEducacionResponse: Nivel de educación actualizado.

    Raises:
        HTTPException: Si el registro no existe.
    """
    nivel_actualizado = update_nivel_educacion(db, id_nivel_educacion, nivel_educacion_data)
    if not nivel_actualizado:
        raise HTTPException(status_code=404, detail="Nivel de educación no encontrado")
    return nivel_actualizado


@router.delete("/{id_nivel_educacion}", response_model=NivelEducacionResponse)
def eliminar_nivel_educacion(id_nivel_educacion: int, db: Session = Depends(get_db)):
    """
    Elimina un nivel de educación por su ID.

    Args:
        id_nivel_educacion (int): ID del nivel a eliminar.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        NivelEducacionResponse: Nivel eliminado.

    Raises:
        HTTPException: Si el registro no existe.
    """
    nivel_eliminado = delete_nivel_educacion(db, id_nivel_educacion)
    if not nivel_eliminado:
        raise HTTPException(status_code=404, detail="Nivel de educación no encontrado")
    return nivel_eliminado
