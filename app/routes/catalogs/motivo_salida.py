from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.catalogs.motivo_salida import MotivoSalidaCreate, MotivoSalidaUpdate, MotivoSalidaResponse
from app.services.catalogs.motivo_salida_service import (
    get_motivos_salida,
    get_motivo_salida,
    create_motivo_salida,
    update_motivo_salida,
    delete_motivo_salida
)

router = APIRouter(prefix="/motivos_salida", tags=["Motivos de Salida"])

@router.get("/", response_model=list[MotivoSalidaResponse])
def obtener_motivos_salida(db: Session = Depends(get_db)):
    return get_motivos_salida(db)

@router.get("/{id_motivo_salida}", response_model=MotivoSalidaResponse)
def obtener_motivo_salida(id_motivo_salida: int, db: Session = Depends(get_db)):
    motivo = get_motivo_salida(db, id_motivo_salida)
    if not motivo:
        raise HTTPException(status_code=404, detail="Motivo de salida no encontrado")
    return motivo

@router.post("/", response_model=MotivoSalidaResponse, status_code=201)
def crear_motivo_salida(motivo_data: MotivoSalidaCreate, db: Session = Depends(get_db)):
    return create_motivo_salida(db, motivo_data)

@router.put("/{id_motivo_salida}", response_model=MotivoSalidaResponse)
def actualizar_motivo_salida(id_motivo_salida: int, motivo_data: MotivoSalidaUpdate, db: Session = Depends(get_db)):
    motivo_actualizado = update_motivo_salida(db, id_motivo_salida, motivo_data)
    if not motivo_actualizado:
        raise HTTPException(status_code=404, detail="Motivo de salida no encontrado")
    return motivo_actualizado

@router.delete("/{id_motivo_salida}", status_code=204)
def eliminar_motivo_salida(id_motivo_salida: int, db: Session = Depends(get_db)):
    if not delete_motivo_salida(db, id_motivo_salida):
        raise HTTPException(status_code=404, detail="Motivo de salida no encontrado")