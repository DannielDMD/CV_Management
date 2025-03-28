"""from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.habilidades_blandas import HabilidadBlanda
from app.schemas.habilidades_blandas import HabilidadBlandaCreate, HabilidadBlandaUpdate

# Obtener todas las habilidades blandas
def get_all_habilidades_blandas(db: Session):
    return db.query(HabilidadBlanda).all()

# Obtener una habilidad blanda por ID
def get_habilidad_blanda(db: Session, id_habilidad_blanda: int):
    habilidad = db.query(HabilidadBlanda).filter(HabilidadBlanda.id_habilidad_blanda == id_habilidad_blanda).first()
    if not habilidad:
        raise HTTPException(status_code=404, detail="Habilidad blanda no encontrada")
    return habilidad

# Crear una nueva habilidad blanda
def create_habilidad_blanda(db: Session, habilidad_data: HabilidadBlandaCreate):
    habilidad_existente = db.query(HabilidadBlanda).filter(HabilidadBlanda.nombre_habilidad == habilidad_data.nombre_habilidad).first()
    if habilidad_existente:
        raise HTTPException(status_code=400, detail="La habilidad blanda ya existe")

    nueva_habilidad = HabilidadBlanda(**habilidad_data.model_dump())
    db.add(nueva_habilidad)
    db.commit()
    db.refresh(nueva_habilidad)
    return nueva_habilidad

# Actualizar una habilidad blanda
def update_habilidad_blanda(db: Session, id_habilidad_blanda: int, habilidad_data: HabilidadBlandaUpdate):
    habilidad = db.query(HabilidadBlanda).filter(HabilidadBlanda.id_habilidad_blanda == id_habilidad_blanda).first()
    if not habilidad:
        raise HTTPException(status_code=404, detail="Habilidad blanda no encontrada")

    habilidad.nombre_habilidad = habilidad_data.nombre_habilidad
    db.commit()
    db.refresh(habilidad)
    return habilidad

# Eliminar una habilidad blanda
def delete_habilidad_blanda(db: Session, id_habilidad_blanda: int):
    habilidad = db.query(HabilidadBlanda).filter(HabilidadBlanda.id_habilidad_blanda == id_habilidad_blanda).first()
    if not habilidad:
        raise HTTPException(status_code=404, detail="Habilidad blanda no encontrada")

    db.delete(habilidad)
    db.commit()
    return {"message": "Habilidad blanda eliminada correctamente"}
"""