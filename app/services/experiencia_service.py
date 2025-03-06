from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.experiencia import ExperienciaLaboral
from app.schemas.experiencia import ExperienciaLaboralCreate, ExperienciaLaboralUpdate

# Crear una experiencia laboral
def create_experiencia(db: Session, experiencia_data: ExperienciaLaboralCreate):
    nueva_experiencia = ExperienciaLaboral(**experiencia_data.model_dump())
    try:
        db.add(nueva_experiencia)
        db.commit()
        db.refresh(nueva_experiencia)
        return nueva_experiencia
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al insertar la experiencia laboral en la base de datos")

# Obtener una experiencia laboral por ID
def get_experiencia_by_id(db: Session, id_experiencia: int):
    experiencia = db.query(ExperienciaLaboral).filter(ExperienciaLaboral.id_experiencia == id_experiencia).first()
    
    if not experiencia:
        raise HTTPException(status_code=404, detail="Experiencia laboral no encontrada")
    
    return experiencia

# Obtener todas las experiencias laborales de un candidato por su ID
def get_experiencias_by_candidato(db: Session, id_candidato: int):
    experiencias = db.query(ExperienciaLaboral).filter(ExperienciaLaboral.id_candidato == id_candidato).all()
    
    if not experiencias:
        raise HTTPException(status_code=404, detail="No se encontraron experiencias laborales para este candidato")
    
    return experiencias


# Obtener todas las experiencias laborales
def get_all_experiencias(db: Session):
    return db.query(ExperienciaLaboral).all()

# Actualizar una experiencia laboral
def update_experiencia(db: Session, id_experiencia: int, experiencia_data: ExperienciaLaboralUpdate):
    experiencia = db.query(ExperienciaLaboral).filter(ExperienciaLaboral.id_experiencia == id_experiencia).first()
    
    if not experiencia:
        raise HTTPException(status_code=404, detail="Experiencia laboral no encontrada")
    
    for key, value in experiencia_data.model_dump(exclude_unset=True).items():
        setattr(experiencia, key, value)
    
    db.commit()
    db.refresh(experiencia)
    
    return experiencia

# Eliminar una experiencia laboral
def delete_experiencia(db: Session, id_experiencia: int):
    experiencia = db.query(ExperienciaLaboral).filter(ExperienciaLaboral.id_experiencia == id_experiencia).first()
    
    if not experiencia:
        raise HTTPException(status_code=404, detail="Experiencia laboral no encontrada")
    
    db.delete(experiencia)
    db.commit()
    
    return {"message": "Experiencia laboral eliminada correctamente"}
