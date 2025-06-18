"""Rutas para la gestión del catálogo de niveles de educación."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.schemas.catalogs.nivel_educacion import (
    NivelEducacionCreate,
    NivelEducacionPaginatedResponse,
    NivelEducacionUpdate,
    NivelEducacionResponse
)
from app.services.catalogs.nivel_educacion_service import (
    get_niveles_educacion, 
    get_nivel_educacion, 
    create_nivel_educacion,
    get_niveles_educacion_con_paginacion, 
    update_nivel_educacion, 
    delete_nivel_educacion
)

router = APIRouter(prefix="/nivel-educacion", tags=["Nivel Educación"])


@router.get("/", response_model=NivelEducacionPaginatedResponse)
def listar_niveles_educacion_con_paginacion(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Lista niveles de educación con búsqueda por nombre y paginación.
    """
    return get_niveles_educacion_con_paginacion(
        db=db,
        skip=skip,
        limit=limit,
        search=search
    )


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
