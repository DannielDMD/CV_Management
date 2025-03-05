from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.preferencias_service import (
    obtener_preferencia_candidato,
    crear_preferencia,
    actualizar_preferencia,
    eliminar_preferencia
)
from app.schemas.preferencias import PreferenciaDisponibilidadCreate, PreferenciaDisponibilidadUpdate, PreferenciaDisponibilidadResponse
from app.core.database import get_db

router = APIRouter(prefix="/preferencias", tags=["Preferencias"])

@router.get("/{id_candidato}", response_model=PreferenciaDisponibilidadResponse)
def get_preferencia(id_candidato: int, db: Session = Depends(get_db)):
    return obtener_preferencia_candidato(db, id_candidato)

@router.post("/", response_model=PreferenciaDisponibilidadResponse)
def create_preferencia(preferencia_data: PreferenciaDisponibilidadCreate, db: Session = Depends(get_db)):
    return crear_preferencia(db, preferencia_data)

@router.put("/{id_candidato}", response_model=PreferenciaDisponibilidadResponse)
def update_preferencia(id_candidato: int, preferencia_data: PreferenciaDisponibilidadUpdate, db: Session = Depends(get_db)):
    return actualizar_preferencia(db, id_candidato, preferencia_data)

@router.delete("/{id_candidato}")
def delete_preferencia(id_candidato: int, db: Session = Depends(get_db)):
    return eliminar_preferencia(db, id_candidato)
