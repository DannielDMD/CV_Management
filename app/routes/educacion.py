from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.educacion_service import (
    create_educacion,
    get_educacion_by_id,
    get_all_educaciones,
    get_educaciones_by_candidato,
    update_educacion,
    delete_educacion
)
from app.schemas.educacion import EducacionCreate, EducacionUpdate, EducacionResponse
from app.core.database import get_db
from typing import List


router = APIRouter(prefix="/educaciones", tags=["Educaciones"])

@router.post("/", response_model=EducacionResponse)
def create_education(educacion_data: EducacionCreate, db: Session = Depends(get_db)):
    return create_educacion(db, educacion_data)

@router.get("/{id}", response_model=EducacionResponse)
def get_education(id: int, db: Session = Depends(get_db)):
    return get_educacion_by_id(db, id)

@router.get("/educaciones/candidato/{id_candidato}", response_model=List[EducacionResponse])
def obtener_educaciones_por_candidato(id_candidato: int, db: Session = Depends(get_db)):
    return get_educaciones_by_candidato(db, id_candidato)

@router.get("/", response_model=list[EducacionResponse])
def get_all_educations(db: Session = Depends(get_db)):
    return get_all_educaciones(db)

@router.put("/{id}", response_model=EducacionResponse)
def update_education(id: int, educacion_data: EducacionUpdate, db: Session = Depends(get_db)):
    return update_educacion(db, id, educacion_data)

@router.delete("/{id}")
def delete_education(id: int, db: Session = Depends(get_db)):
    return delete_educacion(db, id)
