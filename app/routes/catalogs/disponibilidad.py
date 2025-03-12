from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from app.services.catalogs.disponibilidad_service import (
    get_all_disponibilidades,
    get_disponibilidad,
    create_disponibilidad,
    update_disponibilidad,
    delete_disponibilidad
)
from app.schemas.preferencias import DisponibilidadCreate, DisponibilidadUpdate, DisponibilidadResponse
from app.core.database import get_db

router = APIRouter(prefix="/disponibilidades", tags=["Disponibilidad"])

@router.get("/", response_model=list[DisponibilidadResponse])
def listar_disponibilidades(db: Session = Depends(get_db)):
    return get_all_disponibilidades(db)

@router.get("/{disponibilidad_id}", response_model=DisponibilidadResponse)
def obtener_disponibilidad(disponibilidad_id: int, db: Session = Depends(get_db)):
    try:
        return get_disponibilidad(db, disponibilidad_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"Disponibilidad con ID {disponibilidad_id} no encontrada")

@router.post("/", response_model=DisponibilidadResponse)
def crear_disponibilidad(disponibilidad_data: DisponibilidadCreate, db: Session = Depends(get_db)):
    try:
        return create_disponibilidad(db, disponibilidad_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{disponibilidad_id}", response_model=DisponibilidadResponse)
def actualizar_disponibilidad(disponibilidad_id: int, disponibilidad_data: DisponibilidadUpdate, db: Session = Depends(get_db)):
    try:
        return update_disponibilidad(db, disponibilidad_id, disponibilidad_data)
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"Disponibilidad con ID {disponibilidad_id} no encontrada")

@router.delete("/{disponibilidad_id}")
def eliminar_disponibilidad(disponibilidad_id: int, db: Session = Depends(get_db)):
    try:
        return delete_disponibilidad(db, disponibilidad_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"Disponibilidad con ID {disponibilidad_id} no encontrada")
