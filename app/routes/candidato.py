from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.candidato_service import (
    create_candidato, get_candidato_by_id, get_all_candidatos, update_candidato, delete_candidato
)
from app.schemas.candidato import CandidatoCreate, CandidatoUpdate, CandidatoResponse
from app.core.database import get_db
from typing import List

router = APIRouter(prefix="/candidatos", tags=["Candidatos"])

# Crear un candidato
@router.post("/", response_model=CandidatoResponse)
def create(candidato: CandidatoCreate, db: Session = Depends(get_db)):
    return create_candidato(db, candidato)

# Obtener todos los candidatos
@router.get("/", response_model=List[CandidatoResponse])
def get_all(db: Session = Depends(get_db)):
    return get_all_candidatos(db)

# Obtener un candidato por ID
@router.get("/{id_candidato}", response_model=CandidatoResponse)
def get_by_id(id_candidato: int, db: Session = Depends(get_db)):
    return get_candidato_by_id(db, id_candidato)

# Actualizar un candidato
@router.put("/{id_candidato}", response_model=CandidatoResponse)
def update(id_candidato: int, candidato: CandidatoUpdate, db: Session = Depends(get_db)):
    return update_candidato(db, id_candidato, candidato)

# Eliminar un candidato
@router.delete("/{id_candidato}")
def delete(id_candidato: int, db: Session = Depends(get_db)):
    return delete_candidato(db, id_candidato)
