from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.models.conocimientos_model import CandidatoConocimiento
from app.schemas.conocimientos_candidato_schema import CandidatoConocimientoCreate
from app.models.candidato_model import Candidato

def create_conocimiento(db: Session, conocimiento_data: CandidatoConocimientoCreate):
    """Crea un nuevo conocimiento asociado a un candidato."""
    try:
        candidato = db.query(Candidato).filter(Candidato.id_candidato == conocimiento_data.id_candidato).first()
        if not candidato:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Candidato no encontrado")

        nuevo_conocimiento = CandidatoConocimiento(**conocimiento_data.dict())
        db.add(nuevo_conocimiento)
        db.commit()
        db.refresh(nuevo_conocimiento)
        return nuevo_conocimiento
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error de integridad en la base de datos")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno: {str(e)}")

def get_conocimiento(db: Session, id_conocimiento: int):
    """Obtiene un conocimiento específico por su ID."""
    conocimiento = db.query(CandidatoConocimiento).filter(CandidatoConocimiento.id_conocimiento == id_conocimiento).first()
    if not conocimiento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conocimiento no encontrado")
    return conocimiento

def delete_conocimiento(db: Session, id_conocimiento: int):
    """Elimina un conocimiento de un candidato."""
    try:
        conocimiento = db.query(CandidatoConocimiento).filter(CandidatoConocimiento.id_conocimiento == id_conocimiento).first()
        if not conocimiento:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conocimiento no encontrado")
        
        db.delete(conocimiento)
        db.commit()
        return {"message": "Conocimiento eliminado exitosamente"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno: {str(e)}")
