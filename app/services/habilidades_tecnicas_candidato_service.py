from sqlalchemy.orm import Session
from app.models.habilidades_tecnicas import CategoriaHabilidadTecnica, HabilidadTecnica, HabilidadTecnicaCandidato
from app.schemas.habilidades_tecnicas import HabilidadTecnicaCandidatoCreate
from fastapi import HTTPException

def get_all_categorias_habilidades_tecnicas(db: Session):
    return db.query(CategoriaHabilidadTecnica).all()

def get_all_habilidades_tecnicas(db: Session):
    return db.query(HabilidadTecnica).all()

def assign_habilidad_tecnica(db: Session, habilidad_data: HabilidadTecnicaCandidatoCreate):
    # Verificar si la habilidad técnica ya está asignada al candidato
    existing = db.query(HabilidadTecnicaCandidato).filter_by(
        id_candidato=habilidad_data.id_candidato, id_habilidad_tecnica=habilidad_data.id_habilidad_tecnica
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Habilidad técnica ya asignada al candidato")

    nueva_habilidad = HabilidadTecnicaCandidato(
        id_candidato=habilidad_data.id_candidato,
        id_habilidad_tecnica=habilidad_data.id_habilidad_tecnica
    )

    db.add(nueva_habilidad)
    db.commit()
    db.refresh(nueva_habilidad)
    return nueva_habilidad

def get_habilidades_tecnicas_by_candidato(db: Session, id_candidato: int):
    habilidades = db.query(HabilidadTecnicaCandidato).filter_by(id_candidato=id_candidato).all()
    
    if not habilidades:
        raise HTTPException(status_code=404, detail="El candidato no tiene habilidades técnicas registradas")
    
    return habilidades

def remove_habilidad_tecnica(db: Session, id_candidato: int, id_habilidad: int):
    habilidad = db.query(HabilidadTecnicaCandidato).filter_by(
        id_candidato=id_candidato, id_habilidad_tecnica=id_habilidad
    ).first()

    if not habilidad:
        raise HTTPException(status_code=404, detail="Habilidad técnica no encontrada para este candidato")

    db.delete(habilidad)
    db.commit()
    return {"message": "Habilidad técnica eliminada correctamente"}
