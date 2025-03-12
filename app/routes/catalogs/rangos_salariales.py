from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from app.services.catalogs.rangos_salariales_service import (
    get_all_rangos_salariales,
    get_rango_salarial,
    create_rango_salarial,
    update_rango_salarial,
    delete_rango_salarial
)
from app.schemas.preferencias import RangoSalarialCreate, RangoSalarialUpdate, RangoSalarialResponse
from app.core.database import get_db

router = APIRouter(prefix="/rangos-salariales", tags=["Rangos Salariales"])

@router.get("/", response_model=list[RangoSalarialResponse])
def listar_rangos_salariales(db: Session = Depends(get_db)):
    return get_all_rangos_salariales(db)

@router.get("/{rango_id}", response_model=RangoSalarialResponse)
def obtener_rango_salarial(rango_id: int, db: Session = Depends(get_db)):
    try:
        return get_rango_salarial(db, rango_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"Rango Salarial con ID {rango_id} no encontrado")

@router.post("/", response_model=RangoSalarialResponse)
def crear_rango_salarial(rango_data: RangoSalarialCreate, db: Session = Depends(get_db)):
    try:
        return create_rango_salarial(db, rango_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{rango_id}", response_model=RangoSalarialResponse)
def actualizar_rango_salarial(rango_id: int, rango_data: RangoSalarialUpdate, db: Session = Depends(get_db)):
    try:
        return update_rango_salarial(db, rango_id, rango_data)
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"Rango Salarial con ID {rango_id} no encontrado")

@router.delete("/{rango_id}")
def eliminar_rango_salarial(rango_id: int, db: Session = Depends(get_db)):
    try:
        return delete_rango_salarial(db, rango_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"Rango Salarial con ID {rango_id} no encontrado")
