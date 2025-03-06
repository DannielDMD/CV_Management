from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.experiencia_service import (
    create_experiencia,
    get_experiencia_by_id,
    get_all_experiencias,
    get_experiencias_by_candidato,
    update_experiencia,
    delete_experiencia
)
from app.schemas.experiencia import ExperienciaLaboralCreate, ExperienciaLaboralUpdate, ExperienciaLaboralResponse
from app.core.database import get_db
from typing import List

router = APIRouter(prefix="/experiencias", tags=["Experiencias Laborales"])

@router.post("/", response_model=ExperienciaLaboralResponse)
def create_experience(experiencia_data: ExperienciaLaboralCreate, db: Session = Depends(get_db)):
    return create_experiencia(db, experiencia_data)

@router.get("/{id}", response_model=ExperienciaLaboralResponse)
def get_experience(id: int, db: Session = Depends(get_db)):
    return get_experiencia_by_id(db, id)

@router.get("/", response_model=list[ExperienciaLaboralResponse])
def get_all_experiences(db: Session = Depends(get_db)):
    return get_all_experiencias(db)

@router.put("/{id}", response_model=ExperienciaLaboralResponse)
def update_experience(id: int, experiencia_data: ExperienciaLaboralUpdate, db: Session = Depends(get_db)):
    return update_experiencia(db, id, experiencia_data)

@router.get("/candidato/{id_candidato}", response_model=list[ExperienciaLaboralResponse])
def get_experiences_by_candidate(id_candidato: int, db: Session = Depends(get_db)):
    return get_experiencias_by_candidato(db, id_candidato)


@router.delete("/{id}")
def delete_experience(id: int, db: Session = Depends(get_db)):
    return delete_experiencia(db, id)
