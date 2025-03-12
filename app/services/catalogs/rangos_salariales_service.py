from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, NoResultFound
from app.models.preferencias import RangoSalarial
from app.schemas.preferencias import RangoSalarialCreate, RangoSalarialUpdate

def get_all_rangos_salariales(db: Session):
    return db.query(RangoSalarial).all()

def get_rango_salarial(db: Session, rango_id: int):
    rango = db.query(RangoSalarial).filter(RangoSalarial.id_rango_salarial == rango_id).first()
    if not rango:
        raise NoResultFound(f"Rango Salarial con ID {rango_id} no encontrado")
    return rango

def create_rango_salarial(db: Session, rango_data: RangoSalarialCreate):
    try:
        nuevo_rango = RangoSalarial(descripcion_rango=rango_data.descripcion_rango)
        db.add(nuevo_rango)
        db.commit()
        db.refresh(nuevo_rango)
        return nuevo_rango
    except IntegrityError:
        db.rollback()
        raise ValueError("Ya existe un Rango Salarial con esa descripción")

def update_rango_salarial(db: Session, rango_id: int, rango_data: RangoSalarialUpdate):
    rango = get_rango_salarial(db, rango_id)
    if rango_data.descripcion_rango:
        rango.descripcion_rango = rango_data.descripcion_rango
    db.commit()
    db.refresh(rango)
    return rango

def delete_rango_salarial(db: Session, rango_id: int):
    rango = get_rango_salarial(db, rango_id)
    db.delete(rango)
    db.commit()
    return {"message": f"Rango Salarial con ID {rango_id} eliminado correctamente"}
