from sqlalchemy.orm import Session
from app.models.catalogs.ciudad import Ciudad
from app.schemas.catalogs.ciudad import CiudadCreate
from fastapi import HTTPException

# Catalogo de ciudades
def get_ciudades(db: Session):
    return db.query(Ciudad).all()

def get_ciudad_by_id(db: Session, ciudad_id: int):
    ciudad = db.query(Ciudad).filter(Ciudad.id_ciudad == ciudad_id).first()
    if not ciudad:
        raise HTTPException(status_code=404, detail="Ciudad no encontrada")
    return ciudad

def create_ciudad(db: Session, ciudad_data: CiudadCreate):
    # Verificar si la ciudad ya existe
    existing_ciudad = db.query(Ciudad).filter(Ciudad.nombre_ciudad == ciudad_data.nombre_ciudad).first()
    if existing_ciudad:
        raise HTTPException(status_code=400, detail="La ciudad ya existe")

    nueva_ciudad = Ciudad(nombre_ciudad=ciudad_data.nombre_ciudad)
    db.add(nueva_ciudad)
    db.commit()
    db.refresh(nueva_ciudad)
    return nueva_ciudad

def delete_ciudad(db: Session, ciudad_id: int):
    ciudad = db.query(Ciudad).filter(Ciudad.id_ciudad == ciudad_id).first()
    if not ciudad:
        raise HTTPException(status_code=404, detail="Ciudad no encontrada")
    
    db.delete(ciudad)
    db.commit()
    return {"detail": "Ciudad eliminada correctamente"}
