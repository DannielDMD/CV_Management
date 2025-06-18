"""Rutas para la gestión del catálogo de títulos obtenidos."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.schemas.catalogs.titulo import (
    TituloObtenidoCreate,
    TituloObtenidoPaginatedResponse,
    TituloObtenidoUpdate,
    TituloObtenidoResponse
)
from app.services.catalogs.titulo_service import (
    get_titulo,
    get_titulos,
    get_titulos_con_filtros,
    get_titulos_por_nivel,
    create_titulo,
    update_titulo,
    delete_titulo
)

router = APIRouter(prefix="/titulos", tags=["Títulos Obtenidos"])


@router.get("/", response_model=TituloObtenidoPaginatedResponse)
def listar_titulos_con_filtros(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    search: Optional[str] = Query(None),
    id_nivel_educacion: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Lista títulos con búsqueda, paginación y filtro por nivel educativo.
    """
    return get_titulos_con_filtros(
        db=db,
        skip=skip,
        limit=limit,
        search=search,
        id_nivel_educacion=id_nivel_educacion
    )


@router.get("/{titulo_id}", response_model=TituloObtenidoResponse)
def read_titulo(titulo_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un título por su ID.

    Args:
        titulo_id (int): ID del título a consultar.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        TituloObtenidoResponse: Título encontrado.
    """
    return get_titulo(db, titulo_id)


@router.get("/nivel/{id_nivel_educacion}", response_model=List[TituloObtenidoResponse])
def read_titulos_por_nivel(id_nivel_educacion: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Lista títulos filtrados por nivel educativo.

    Args:
        id_nivel_educacion (int): ID del nivel educativo.
        skip (int): Número de registros a omitir (paginación).
        limit (int): Número máximo de registros a retornar.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        List[TituloObtenidoResponse]: Lista de títulos asociados al nivel.
    """
    return get_titulos_por_nivel(db, id_nivel_educacion, skip, limit)


@router.post("/", response_model=TituloObtenidoResponse, status_code=201)
def create_titulo_endpoint(titulo: TituloObtenidoCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo título obtenido.

    Args:
        titulo (TituloObtenidoCreate): Datos del título.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        TituloObtenidoResponse: Título creado.
    """
    return create_titulo(db, titulo)


@router.put("/{titulo_id}", response_model=TituloObtenidoResponse)
def update_titulo_endpoint(titulo_id: int, titulo_update: TituloObtenidoUpdate, db: Session = Depends(get_db)):
    """
    Actualiza un título existente.

    Args:
        titulo_id (int): ID del título a actualizar.
        titulo_update (TituloObtenidoUpdate): Nuevos datos del título.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        TituloObtenidoResponse: Título actualizado.
    """
    return update_titulo(db, titulo_id, titulo_update)


@router.delete("/{titulo_id}")
def delete_titulo_endpoint(titulo_id: int, db: Session = Depends(get_db)):
    """
    Elimina un título por su ID.

    Args:
        titulo_id (int): ID del título a eliminar.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        dict: Mensaje de confirmación.
    """
    return delete_titulo(db, titulo_id)
