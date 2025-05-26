"""
Servicios para la gestión de conocimientos (habilidades blandas, técnicas y herramientas)
asociados a un candidato.
"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.models.conocimientos_model import CandidatoConocimiento
from app.schemas.conocimientos_candidato_schema import CandidatoConocimientoCreate
from app.models.candidato_model import Candidato


def create_conocimiento(db: Session, conocimiento_data: CandidatoConocimientoCreate) -> CandidatoConocimiento:
    """
    Crea un nuevo conocimiento (blando, técnico o herramienta) asociado a un candidato específico.

    Args:
        db (Session): Sesión activa de la base de datos.
        conocimiento_data (CandidatoConocimientoCreate): Datos del conocimiento a registrar.

    Returns:
        CandidatoConocimiento: Objeto del conocimiento creado.

    Raises:
        HTTPException: 
            - 404 si el candidato no existe.
            - 400 si hay un error de integridad en la base de datos.
            - 500 si ocurre un error inesperado durante la operación.
    """
    try:
        candidato = db.query(Candidato).filter(Candidato.id_candidato == conocimiento_data.id_candidato).first()
        if not candidato:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Candidato no encontrado"
            )

        nuevo_conocimiento = CandidatoConocimiento(**conocimiento_data.model_dump())
        db.add(nuevo_conocimiento)
        db.commit()
        db.refresh(nuevo_conocimiento)
        return nuevo_conocimiento

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error de integridad en la base de datos"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno: {str(e)}"
        )


def get_conocimiento(db: Session, id_conocimiento: int) -> CandidatoConocimiento:
    """
    Recupera un conocimiento registrado a partir de su ID.

    Args:
        db (Session): Sesión activa de la base de datos.
        id_conocimiento (int): Identificador único del conocimiento.

    Returns:
        CandidatoConocimiento: Objeto del conocimiento recuperado.

    Raises:
        HTTPException: 404 si el conocimiento no se encuentra.
    """
    conocimiento = (
        db.query(CandidatoConocimiento)
        .filter(CandidatoConocimiento.id_conocimiento == id_conocimiento)
        .first()
    )
    if not conocimiento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conocimiento no encontrado"
        )
    return conocimiento


def delete_conocimiento(db: Session, id_conocimiento: int) -> dict:
    """
    Elimina un conocimiento específico a partir de su ID.

    Args:
        db (Session): Sesión activa de la base de datos.
        id_conocimiento (int): Identificador del conocimiento a eliminar.

    Returns:
        dict: Mensaje de confirmación de eliminación.

    Raises:
        HTTPException: 
            - 404 si el conocimiento no existe.
            - 500 si ocurre un error inesperado durante la eliminación.
    """
    try:
        conocimiento = (
            db.query(CandidatoConocimiento)
            .filter(CandidatoConocimiento.id_conocimiento == id_conocimiento)
            .first()
        )
        if not conocimiento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conocimiento no encontrado"
            )
        
        db.delete(conocimiento)
        db.commit()
        return {"message": "Conocimiento eliminado exitosamente"}

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno: {str(e)}"
        )
