import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.candidato import Candidato
from app.schemas.candidato import CandidatoCreate, CandidatoUpdate

# Configurar logging
logger = logging.getLogger(__name__)

# Crear un candidato
def create_candidato(db: Session, candidato_data: CandidatoCreate):
    # Verificar si el correo ya existe
    if db.query(Candidato).filter(Candidato.correo_electronico == candidato_data.correo_electronico).first():
        raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado")
    
    nuevo_candidato = Candidato(**candidato_data.model_dump())

    try:
        db.add(nuevo_candidato)
        db.commit()
        db.refresh(nuevo_candidato)
        return nuevo_candidato
    except IntegrityError as e:
        logger.error(f"Error de integridad al insertar candidato: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al insertar el candidato en la base de datos")

# Obtener un candidato por ID
def get_candidato_by_id(db: Session, id_candidato: int):
    candidato = db.get(Candidato, id_candidato)
    if not candidato:
        raise HTTPException(status_code=404, detail="Candidato no encontrado")
    return candidato

# Obtener todos los candidatos
def get_all_candidatos(db: Session):
    return db.query(Candidato).all()

# Actualizar un candidato
def update_candidato(db: Session, id_candidato: int, candidato_data: CandidatoUpdate):
    candidato = db.get(Candidato, id_candidato)
    if not candidato:
        raise HTTPException(status_code=404, detail="Candidato no encontrado")

    cambios = candidato_data.model_dump(exclude_unset=True)
    if not cambios:
        raise HTTPException(status_code=400, detail="No hay datos para actualizar")

    for key, value in cambios.items():
        setattr(candidato, key, value)

    try:
        db.commit()
        db.refresh(candidato)
        return candidato
    except IntegrityError as e:
        logger.error(f"Error al actualizar candidato: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al actualizar el candidato en la base de datos")

# Eliminar un candidato
def delete_candidato(db: Session, id_candidato: int):
    candidato = db.get(Candidato, id_candidato)
    if not candidato:
        raise HTTPException(status_code=404, detail="Candidato no encontrado")

    db.delete(candidato)
    try:
        db.commit()
        return {"message": f"Candidato {candidato.nombre_completo} eliminado correctamente"}
    except Exception as e:
        logger.error(f"Error al eliminar candidato: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al eliminar el candidato")
