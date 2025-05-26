"""Rutas para consultar los catálogos de conocimientos (habilidades y herramientas)."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.services.catalogs.conocimientos_service import (
    get_habilidades_blandas,
    get_habilidades_tecnicas,
    get_herramientas
)
from app.schemas.catalogs.conocimientos_schema import (
    HabilidadBlandaResponse,
    HabilidadTecnicaResponse,
    HerramientaResponse
)

router = APIRouter(prefix="/conocimientos", tags=["Conocimientos"])

@router.get("/habilidades-blandas", response_model=List[HabilidadBlandaResponse])
def obtener_habilidades_blandas(db: Session = Depends(get_db)):
    """
    Lista todas las habilidades blandas disponibles.

    Args:
        db (Session): Sesión de base de datos inyectada.

    Returns:
        List[HabilidadBlandaResponse]: Lista de habilidades blandas.
    """
    return get_habilidades_blandas(db)

@router.get("/habilidades-tecnicas", response_model=List[HabilidadTecnicaResponse])
def obtener_habilidades_tecnicas(db: Session = Depends(get_db)):
    """
    Lista todas las habilidades técnicas disponibles.

    Args:
        db (Session): Sesión de base de datos inyectada.

    Returns:
        List[HabilidadTecnicaResponse]: Lista de habilidades técnicas.
    """
    return get_habilidades_tecnicas(db)

@router.get("/herramientas", response_model=List[HerramientaResponse])
def obtener_herramientas(db: Session = Depends(get_db)):
    """
    Lista todas las herramientas disponibles.

    Args:
        db (Session): Sesión de base de datos inyectada.

    Returns:
        List[HerramientaResponse]: Lista de herramientas.
    """
    return get_herramientas(db)
