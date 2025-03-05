from sqlalchemy.orm import Session
from app.models.preferencias import PreferenciaDisponibilidad
from app.schemas.preferencias import PreferenciaDisponibilidadCreate, PreferenciaDisponibilidadUpdate, PreferenciaDisponibilidadResponse

def obtener_preferencia_candidato(db: Session, id_candidato: int):
    return db.query(PreferenciaDisponibilidad).filter(PreferenciaDisponibilidad.id_candidato == id_candidato).first()

def crear_preferencia(db: Session, preferencia_data: PreferenciaDisponibilidadCreate):
    nueva_preferencia = PreferenciaDisponibilidad(**preferencia_data.dict())
    db.add(nueva_preferencia)
    db.commit()
    db.refresh(nueva_preferencia)
    return nueva_preferencia

def actualizar_preferencia(db: Session, id_candidato: int, preferencia_data: PreferenciaDisponibilidadUpdate):
    preferencia = obtener_preferencia_candidato(db, id_candidato)
    if not preferencia:
        return None
    
    for key, value in preferencia_data.dict(exclude_unset=True).items():
        setattr(preferencia, key, value)
    
    db.commit()
    db.refresh(preferencia)
    return preferencia

def eliminar_preferencia(db: Session, id_candidato: int):
    preferencia = obtener_preferencia_candidato(db, id_candidato)
    if not preferencia:
        return None
    
    db.delete(preferencia)
    db.commit()
    return True  # Devuelve True si se eliminó correctamente
