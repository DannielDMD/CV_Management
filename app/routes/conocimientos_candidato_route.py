"""Rutas para la gestión de conocimientos asociados a un candidato."""

from typing import List
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.conocimientos_candidato_schema import (
    CandidatoConocimientoCreate,
    CandidatoConocimientoResponse
)
from app.services.conocimientos_candidato_service import (
    get_conocimiento,
    create_conocimiento,
    delete_conocimiento
)

router = APIRouter(
    prefix="/conocimientos-candidato",
    tags=["Conocimientos Candidato"]
)


@router.post("/", status_code=201)
def create_conocimientos_endpoint(
    conocimientos: List[CandidatoConocimientoCreate],
    db: Session = Depends(get_db)
):
    """
    Crea múltiples conocimientos asociados a un candidato.

    Args:
        conocimientos (List[CandidatoConocimientoCreate]): Lista de conocimientos a registrar.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        JSONResponse: Número de conocimientos creados exitosamente.
    """
    creados = [create_conocimiento(db, conocimiento) for conocimiento in conocimientos]
    return JSONResponse(content={"detalles": f"{len(creados)} conocimientos creados con éxito"})


@router.get("/{conocimiento_id}", response_model=CandidatoConocimientoResponse)
def get_conocimiento_endpoint(conocimiento_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un conocimiento específico por su ID.

    Args:
        conocimiento_id (int): ID del conocimiento.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        CandidatoConocimientoResponse: Detalle del conocimiento registrado.
    """
    return get_conocimiento(db, conocimiento_id)


@router.delete("/{conocimiento_id}", status_code=204)
def delete_conocimiento_endpoint(conocimiento_id: int, db: Session = Depends(get_db)):
    """
    Elimina un conocimiento del candidato por su ID.

    Args:
        conocimiento_id (int): ID del conocimiento a eliminar.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        None: Código HTTP 204 (sin contenido).
    """
    delete_conocimiento(db, conocimiento_id)
    return None
