from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.habilidades_blandas import HabilidadBlanda, HabilidadBlandaCandidato
from app.schemas.habilidades_blandas import HabilidadBlandaCandidatoCreate

"""# Obtener todas las habilidades blandas (catálogo)
def get_all_habilidades_blandas(db: Session):
    return db.query(HabilidadBlanda).all()"""

# Asignar una habilidad blanda a un candidato
def assign_habilidad_blanda(db: Session, habilidad_data: HabilidadBlandaCandidatoCreate):
    # Verificar si ya está asignada
    existing_record = db.query(HabilidadBlandaCandidato).filter(
        HabilidadBlandaCandidato.id_candidato == habilidad_data.id_candidato,
        HabilidadBlandaCandidato.id_habilidad_blanda == habilidad_data.id_habilidad_blanda
    ).first()

    if existing_record:
        raise HTTPException(status_code=400, detail="El candidato ya tiene esta habilidad blanda asignada")

    new_habilidad = HabilidadBlandaCandidato(**habilidad_data.model_dump())
    db.add(new_habilidad)
    db.commit()
    db.refresh(new_habilidad)
    return new_habilidad

# Obtener todas las habilidades blandas de un candidato
def get_habilidades_blandas_by_candidato(db: Session, id_candidato: int):
    habilidades = db.query(HabilidadBlandaCandidato).filter(
        HabilidadBlandaCandidato.id_candidato == id_candidato
    ).all()
    
    if not habilidades:
        raise HTTPException(status_code=404, detail="El candidato no tiene habilidades blandas registradas")

    return habilidades

# Eliminar una habilidad blanda de un candidato
def remove_habilidad_blanda(db: Session, id_candidato: int, id_habilidad_blanda: int):
    habilidad = db.query(HabilidadBlandaCandidato).filter(
        HabilidadBlandaCandidato.id_candidato == id_candidato,
        HabilidadBlandaCandidato.id_habilidad_blanda == id_habilidad_blanda
    ).first()
    
    if not habilidad:
        raise HTTPException(status_code=404, detail="La habilidad blanda no está asignada a este candidato")

    db.delete(habilidad)
    db.commit()
    
    return {"message": "Habilidad blanda eliminada correctamente"}
