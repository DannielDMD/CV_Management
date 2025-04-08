from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.services.candidato_service import (
    create_candidato,
    get_candidato_by_id,
    get_all_candidatos,
    update_candidato,
    delete_candidato,
)
from app.schemas.candidato_schema import CandidatoCreate, CandidatoUpdate, CandidatoResponse
from app.core.database import get_db
from app.services.candidato_service import get_candidatos_resumen
from app.schemas.candidato_schema import CandidatoResumenResponse



router = APIRouter(prefix="/candidatos", tags=["Candidatos"])

# Crear un candidato
@router.post("/", response_model=CandidatoResponse, status_code=status.HTTP_201_CREATED)
def create_candidato_endpoint(candidato_data: CandidatoCreate, db: Session = Depends(get_db)):
    return create_candidato(db, candidato_data)


# Obtener resumen de candidatos (para dashboard)
@router.get("/resumen", response_model=list[CandidatoResumenResponse])
def obtener_resumen_candidatos(db: Session = Depends(get_db)):
    return get_candidatos_resumen(db)



# Obtener un candidato por ID
@router.get("/{id_candidato}", response_model=CandidatoResponse)
def get_candidato_by_id_endpoint(id_candidato: int, db: Session = Depends(get_db)):
    return get_candidato_by_id(db, id_candidato)

# Obtener todos los candidatos
@router.get("/", response_model=list[CandidatoResponse])
def get_all_candidatos_endpoint(db: Session = Depends(get_db)):
    return get_all_candidatos(db)

# Actualizar un candidato
@router.put("/{id_candidato}", response_model=CandidatoResponse)
def update_candidato_endpoint(id_candidato: int, candidato_data: CandidatoUpdate, db: Session = Depends(get_db)):
    return update_candidato(db, id_candidato, candidato_data)

# Eliminar un candidato
@router.delete("/{id_candidato}")
def delete_candidato_endpoint(id_candidato: int, db: Session = Depends(get_db)):
    return delete_candidato(db, id_candidato)
