from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.educacion import Educacion
from app.schemas.educacion import EducacionCreate, EducacionUpdate

#  Crear una educación para un candidato
def create_educacion(db: Session, educacion_data: EducacionCreate):
    nueva_educacion = Educacion(**educacion_data.model_dump())
    try:
        db.add(nueva_educacion)
        db.commit()
        db.refresh(nueva_educacion)
        return nueva_educacion
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al insertar la educación en la base de datos")

#  Obtener una educación por ID
def get_educacion_by_id(db: Session, id_educacion: int):
    educacion = db.query(Educacion).filter(Educacion.id_educacion == id_educacion).first()
    
    if not educacion:
        raise HTTPException(status_code=404, detail="Educación no encontrada")
    
    return educacion

#  Obtener todas las educaciones
def get_all_educaciones(db: Session):
    return db.query(Educacion).all()


# Obtener todas las educaciones de un candidato por su ID
def get_educaciones_by_candidato(db: Session, id_candidato: int):
    educaciones = db.query(Educacion).filter(Educacion.id_candidato == id_candidato).all()
    
    if not educaciones:
        raise HTTPException(status_code=404, detail="No se encontraron educaciones para este candidato")
    
    return educaciones

#  Actualizar una educación
def update_educacion(db: Session, id_educacion: int, educacion_data: EducacionUpdate):
    educacion = db.query(Educacion).filter(Educacion.id_educacion == id_educacion).first()
    
    if not educacion:
        raise HTTPException(status_code=404, detail="Educación no encontrada")
    
    for key, value in educacion_data.model_dump(exclude_unset=True).items():
        setattr(educacion, key, value)
    
    db.commit()
    db.refresh(educacion)
    
    return educacion

#  Eliminar una educación
def delete_educacion(db: Session, id_educacion: int):
    educacion = db.query(Educacion).filter(Educacion.id_educacion == id_educacion).first()
    
    if not educacion:
        raise HTTPException(status_code=404, detail="Educación no encontrada")
    
    db.delete(educacion)
    db.commit()
    
    return {"message": "Educación eliminada correctamente"}
