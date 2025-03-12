from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.catalogs.rango_experiencia import RangoExperiencia
from app.schemas.catalogs.rango_experiencia import RangoExperienciaCreate, RangoExperienciaUpdate

# Obtener todos los rangos de experiencia
def get_rangos_experiencia(db: Session):
    return db.query(RangoExperiencia).all()

# Obtener un rango de experiencia por ID
def get_rango_experiencia(db: Session, rango_experiencia_id: int):
    rango = db.query(RangoExperiencia).filter(RangoExperiencia.id_rango_experiencia == rango_experiencia_id).first()
    if not rango:
        raise HTTPException(status_code=404, detail="Rango de experiencia no encontrado")
    return rango

# Crear un nuevo rango de experiencia
def create_rango_experiencia(db: Session, rango_data: RangoExperienciaCreate):
    existe_rango = db.query(RangoExperiencia).filter(RangoExperiencia.descripcion_rango == rango_data.descripcion_rango).first()
    if existe_rango:
        raise HTTPException(status_code=400, detail="El rango de experiencia ya existe")

    nuevo_rango = RangoExperiencia(descripcion_rango=rango_data.descripcion_rango)
    db.add(nuevo_rango)
    db.commit()
    db.refresh(nuevo_rango)
    return nuevo_rango

# Actualizar un rango de experiencia por ID
def update_rango_experiencia(db: Session, rango_experiencia_id: int, rango_data: RangoExperienciaUpdate):
    rango = db.query(RangoExperiencia).filter(RangoExperiencia.id_rango_experiencia == rango_experiencia_id).first()
    if not rango:
        raise HTTPException(status_code=404, detail="Rango de experiencia no encontrado")

    if rango_data.descripcion_rango:
        rango.descripcion_rango = rango_data.descripcion_rango

    db.commit()
    db.refresh(rango)
    return rango

# Eliminar un rango de experiencia por ID
def delete_rango_experiencia(db: Session, rango_experiencia_id: int):
    rango = db.query(RangoExperiencia).filter(RangoExperiencia.id_rango_experiencia == rango_experiencia_id).first()
    if not rango:
        raise HTTPException(status_code=404, detail="Rango de experiencia no encontrado")

    db.delete(rango)
    db.commit()
    return {"message": "Rango de experiencia eliminado correctamente"}
