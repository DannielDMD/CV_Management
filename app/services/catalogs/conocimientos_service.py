"""
Servicios para la gestión de conocimientos del candidato:
Habilidades blandas, técnicas y herramientas.
Incluye validación de errores y ordenamiento alfabético.
"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

from app.models.conocimientos_model import HabilidadBlanda, HabilidadTecnica, Herramienta
from app.schemas.catalogs.conocimientos_schema import (
    HabilidadBlandaResponse,
    HabilidadTecnicaResponse,
    HerramientaResponse,
)
from app.utils.orden_catalogos import ordenar_por_nombre


def get_habilidades_blandas(db: Session):
    """
    Retorna una lista de habilidades blandas ordenadas alfabéticamente.

    Args:
        db (Session): Sesión activa de la base de datos.

    Returns:
        List[HabilidadBlandaResponse]: Lista de habilidades blandas.

    Raises:
        HTTPException: Si ocurre un error de base de datos o no se encuentran resultados.
    """
    try:
        query = db.query(HabilidadBlanda)
        ordenado = ordenar_por_nombre(query, "nombre_habilidad_blanda").all()
        if not ordenado:
            raise HTTPException(status_code=404, detail="No se encontraron habilidades blandas")
        return [HabilidadBlandaResponse.model_validate(h) for h in ordenado]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener habilidades blandas: {str(e)}")


def get_habilidades_tecnicas(db: Session):
    """
    Retorna una lista de habilidades técnicas ordenadas alfabéticamente.

    Args:
        db (Session): Sesión activa de la base de datos.

    Returns:
        List[HabilidadTecnicaResponse]: Lista de habilidades técnicas.

    Raises:
        HTTPException: Si ocurre un error de base de datos o no se encuentran resultados.
    """
    try:
        query = db.query(HabilidadTecnica)
        ordenado = ordenar_por_nombre(query, "nombre_habilidad_tecnica").all()
        if not ordenado:
            raise HTTPException(status_code=404, detail="No se encontraron habilidades técnicas")
        return [HabilidadTecnicaResponse.model_validate(h) for h in ordenado]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener habilidades técnicas: {str(e)}")


def get_herramientas(db: Session):
    """
    Retorna una lista de herramientas ordenadas alfabéticamente.

    Args:
        db (Session): Sesión activa de la base de datos.

    Returns:
        List[HerramientaResponse]: Lista de herramientas.

    Raises:
        HTTPException: Si ocurre un error de base de datos o no se encuentran resultados.
    """
    try:
        query = db.query(Herramienta)
        ordenado = ordenar_por_nombre(query, "nombre_herramienta").all()
        if not ordenado:
            raise HTTPException(status_code=404, detail="No se encontraron herramientas")
        return [HerramientaResponse.model_validate(h) for h in ordenado]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener herramientas: {str(e)}")
