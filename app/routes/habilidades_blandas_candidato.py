"""from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.habilidades_blandas_candidato_service import (
    assign_habilidades_blandas,
    get_habilidades_blandas_by_candidato,
    remove_habilidad_blanda
)
from app.schemas.habilidades_blandas import (
    HabilidadBlandaCandidatoCreate,
    HabilidadBlandaCandidatoListResponse
)
from app.core.database import get_db

router = APIRouter(prefix="/habilidades-blandas-candidato", tags=["Habilidades Blandas Candidato"])
@router.post("/asignar", response_model=HabilidadBlandaCandidatoListResponse)
def assign_soft_skills(habilidad_data: HabilidadBlandaCandidatoCreate, db: Session = Depends(get_db)):
    return assign_habilidades_blandas(db, habilidad_data)

@router.get("/candidato/{id_candidato}", response_model=HabilidadBlandaCandidatoListResponse)
def get_soft_skills_by_candidate(id_candidato: int, db: Session = Depends(get_db)):
    return get_habilidades_blandas_by_candidato(db, id_candidato)

# Eliminar una habilidad blanda de un candidato
@router.delete("/candidato/{id_candidato}/{id_habilidad}")
def delete_soft_skill(id_candidato: int, id_habilidad: int, db: Session = Depends(get_db)):
    return remove_habilidad_blanda(db, id_candidato, id_habilidad)
"""