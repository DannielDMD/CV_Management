from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.experiencia_service import (
    create_experiencia,
    get_experiencia_by_id,
    get_all_experiencias,
    update_experiencia,
    delete_experiencia
)
from app.schemas.experiencia import ExperienciaLaboralCreate, ExperienciaLaboralUpdate, ExperienciaLaboralResponse
from app.core.database import get_db

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

@router.delete("/{id}")
def delete_experience(id: int, db: Session = Depends(get_db)):
    return delete_experiencia(db, id)
