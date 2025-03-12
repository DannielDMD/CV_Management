from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.habilidades_blandas_candidato_service import (
    assign_habilidad_blanda,
    get_habilidades_blandas_by_candidato,
    remove_habilidad_blanda
)
from app.schemas.habilidades_blandas import HabilidadBlandaCandidatoCreate, HabilidadBlandaCandidatoResponse, HabilidadBlandaResponse
from app.core.database import get_db

router = APIRouter(prefix="/habilidades-blandas-candidato", tags=["Habilidades Blandas Candidato"])

"""@router.get("/", response_model=list[HabilidadBlandaResponse])
def get_all_soft_skills(db: Session = Depends(get_db)):
    return get_all_habilidades_blandas(db)"""

@router.post("/asignar", response_model=HabilidadBlandaCandidatoResponse)
def assign_soft_skill(habilidad_data: HabilidadBlandaCandidatoCreate, db: Session = Depends(get_db)):
    return assign_habilidad_blanda(db, habilidad_data)

@router.get("/candidato/{id}", response_model=list[HabilidadBlandaCandidatoResponse])
def get_soft_skills_by_candidate(id: int, db: Session = Depends(get_db)):
    return get_habilidades_blandas_by_candidato(db, id)

@router.delete("/candidato/{id_candidato}/{id_habilidad}")
def delete_soft_skill(id_candidato: int, id_habilidad: int, db: Session = Depends(get_db)):
    return remove_habilidad_blanda(db, id_candidato, id_habilidad)
