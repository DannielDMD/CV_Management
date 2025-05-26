"""Rutas para la gestión del catálogo de niveles de inglés."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.catalogs.nivel_ingles import (
    NivelInglesResponse,
    NivelInglesCreate,
    NivelInglesUpdate
)
from app.services.catalogs.nivel_ingles_service import (
    get_niveles_ingles,
    get_nivel_ingles,
    create_nivel_ingles,
    update_nivel_ingles,
    delete_nivel_ingles
)

router = APIRouter(prefix="/nivel-ingles", tags=["Nivel de Inglés"])


@router.get("/", response_model=List[NivelInglesResponse])
def listar_niveles_ingles(db: Session = Depends(get_db)):
    """
    Lista todos los niveles de inglés registrados.

    Args:
        db (Session): Sesión de base de datos inyectada.

    Returns:
        List[NivelInglesResponse]: Lista de niveles.
    """
    return get_niveles_ingles(db)


@router.get("/{nivel_ingles_id}", response_model=NivelInglesResponse)
def obtener_nivel_ingles(nivel_ingles_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un nivel de inglés por su ID.

    Args:
        nivel_ingles_id (int): ID del nivel a consultar.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        NivelInglesResponse: Nivel encontrado.
    """
    return get_nivel_ingles(db, nivel_ingles_id)


@router.post("/", response_model=NivelInglesResponse)
def crear_nivel_ingles(nivel_ingles_data: NivelInglesCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo nivel de inglés.

    Args:
        nivel_ingles_data (NivelInglesCreate): Datos del nuevo nivel.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        NivelInglesResponse: Nivel creado.
    """
    return create_nivel_ingles(db, nivel_ingles_data)


@router.put("/{nivel_ingles_id}", response_model=NivelInglesResponse)
def actualizar_nivel_ingles(
    nivel_ingles_id: int,
    nivel_ingles_data: NivelInglesUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualiza un nivel de inglés existente por su ID.

    Args:
        nivel_ingles_id (int): ID del nivel a actualizar.
        nivel_ingles_data (NivelInglesUpdate): Nuevos datos.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        NivelInglesResponse: Nivel actualizado.
    """
    return update_nivel_ingles(db, nivel_ingles_id, nivel_ingles_data)


@router.delete("/{nivel_ingles_id}")
def eliminar_nivel_ingles(nivel_ingles_id: int, db: Session = Depends(get_db)):
    """
    Elimina un nivel de inglés por su ID.

    Args:
        nivel_ingles_id (int): ID del nivel a eliminar.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        dict: Mensaje de confirmación.
    """
    return delete_nivel_ingles(db, nivel_ingles_id)
