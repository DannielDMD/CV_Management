from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, NoResultFound
from app.models.preferencias import Disponibilidad
from app.schemas.preferencias_schema import DisponibilidadCreate, DisponibilidadUpdate

def get_all_disponibilidades(db: Session):
    return db.query(Disponibilidad).all()

def get_disponibilidad(db: Session, disponibilidad_id: int):
    disponibilidad = db.query(Disponibilidad).filter(Disponibilidad.id_disponibilidad == disponibilidad_id).first()
    if not disponibilidad:
        raise NoResultFound(f"Disponibilidad con ID {disponibilidad_id} no encontrada")
    return disponibilidad

def create_disponibilidad(db: Session, disponibilidad_data: DisponibilidadCreate):
    try:
        nueva_disponibilidad = Disponibilidad(descripcion_disponibilidad=disponibilidad_data.descripcion_disponibilidad)
        db.add(nueva_disponibilidad)
        db.commit()
        db.refresh(nueva_disponibilidad)
        return nueva_disponibilidad
    except IntegrityError:
        db.rollback()
        raise ValueError("Ya existe una Disponibilidad con esa descripción")

def update_disponibilidad(db: Session, disponibilidad_id: int, disponibilidad_data: DisponibilidadUpdate):
    disponibilidad = get_disponibilidad(db, disponibilidad_id)
    if disponibilidad_data.descripcion_disponibilidad:
        disponibilidad.descripcion_disponibilidad = disponibilidad_data.descripcion_disponibilidad
    db.commit()
    db.refresh(disponibilidad)
    return disponibilidad

def delete_disponibilidad(db: Session, disponibilidad_id: int):
    disponibilidad = get_disponibilidad(db, disponibilidad_id)
    db.delete(disponibilidad)
    db.commit()
    return {"message": f"Disponibilidad con ID {disponibilidad_id} eliminada correctamente"}
