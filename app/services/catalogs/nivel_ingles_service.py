from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.catalogs.nivel_ingles import NivelIngles
from app.schemas.catalogs.nivel_ingles import NivelInglesCreate, NivelInglesUpdate


# Obtener todos los niveles de inglés
def get_niveles_ingles(db: Session):
     return db.query(NivelIngles).all()

# Obtener un nivel de inglés por ID
def get_nivel_ingles(db: Session, nivel_ingles_id: int):
    nivel_ingles = db.query(NivelIngles).filter(NivelIngles.id_nivel_ingles == nivel_ingles_id).first()
    if not nivel_ingles:
        raise HTTPException(status_code=404, detail="Nivel de inglés no encontrado")
    return nivel_ingles

# Crear un nuevo nivel de inglés
def create_nivel_ingles(db: Session, nivel_ingles_data: NivelInglesCreate):
    existe_nivel = db.query(NivelIngles).filter(NivelIngles.nivel == nivel_ingles_data.nivel).first()
    if existe_nivel:
        raise HTTPException(status_code=400, detail="El nivel de inglés ya existe")

    nuevo_nivel = NivelIngles(nivel=nivel_ingles_data.nivel)
    db.add(nuevo_nivel)
    db.commit()
    db.refresh(nuevo_nivel)
    return nuevo_nivel

# Actualizar un nivel de inglés por ID
def update_nivel_ingles(db: Session, nivel_ingles_id: int, nivel_ingles_data: NivelInglesUpdate):
    nivel_ingles = db.query(NivelIngles).filter(NivelIngles.id_nivel_ingles == nivel_ingles_id).first()
    if not nivel_ingles:
        raise HTTPException(status_code=404, detail="Nivel de inglés no encontrado")

    nivel_ingles.nivel = nivel_ingles_data.nivel
    db.commit()
    db.refresh(nivel_ingles)
    return nivel_ingles

# Eliminar un nivel de inglés por ID
def delete_nivel_ingles(db: Session, nivel_ingles_id: int):
    nivel_ingles = db.query(NivelIngles).filter(NivelIngles.id_nivel_ingles == nivel_ingles_id).first()
    if not nivel_ingles:
        raise HTTPException(status_code=404, detail="Nivel de inglés no encontrado")

    db.delete(nivel_ingles)
    db.commit()
    return {"message": "Nivel de inglés eliminado correctamente"}
