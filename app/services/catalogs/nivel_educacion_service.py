from sqlalchemy.orm import Session
from app.models.catalogs.nivel_educacion import NivelEducacion
from app.schemas.catalogs.nivel_educacion import NivelEducacionCreate, NivelEducacionUpdate

# Obtener todos los niveles de educación
def get_niveles_educacion(db: Session, skip: int = 0, limit: int = 10):
    return db.query(NivelEducacion).offset(skip).limit(limit).all()

# Obtener un nivel de educación por ID
def get_nivel_educacion(db: Session, id_nivel_educacion: int):
    return db.query(NivelEducacion).filter(NivelEducacion.id_nivel_educacion == id_nivel_educacion).first()

# Crear un nuevo nivel de educación
def create_nivel_educacion(db: Session, nivel_educacion_data: NivelEducacionCreate):
    nuevo_nivel = NivelEducacion(**nivel_educacion_data.dict())
    db.add(nuevo_nivel)
    db.commit()
    db.refresh(nuevo_nivel)
    return nuevo_nivel

# Actualizar un nivel de educación existente
def update_nivel_educacion(db: Session, id_nivel_educacion: int, nivel_educacion_data: NivelEducacionUpdate):
    nivel = db.query(NivelEducacion).filter(NivelEducacion.id_nivel_educacion == id_nivel_educacion).first()
    if not nivel:
        return None
    for key, value in nivel_educacion_data.dict(exclude_unset=True).items():
        setattr(nivel, key, value)
    db.commit()
    db.refresh(nivel)
    return nivel

# Eliminar un nivel de educación
def delete_nivel_educacion(db: Session, id_nivel_educacion: int):
    nivel = db.query(NivelEducacion).filter(NivelEducacion.id_nivel_educacion == id_nivel_educacion).first()
    if not nivel:
        return None
    db.delete(nivel)
    db.commit()
    return nivel
