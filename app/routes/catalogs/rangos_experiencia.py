from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.catalogs.rango_experiencia_service import (
    get_rangos_experiencia, get_rango_experiencia,
    create_rango_experiencia, update_rango_experiencia, delete_rango_experiencia
)
from app.schemas.catalogs.rango_experiencia import RangoExperienciaResponse, RangoExperienciaCreate, RangoExperienciaUpdate
from typing import List

router = APIRouter(prefix="/rangos-experiencia", tags=["Rangos de Experiencia"])

# Obtener todos los rangos de experiencia
@router.get("/", response_model=List[RangoExperienciaResponse])
def listar_rangos_experiencia(db: Session = Depends(get_db)):
    return get_rangos_experiencia(db)

# Obtener un rango de experiencia por ID
@router.get("/{rango_experiencia_id}", response_model=RangoExperienciaResponse)
def obtener_rango_experiencia(rango_experiencia_id: int, db: Session = Depends(get_db)):
    return get_rango_experiencia(db, rango_experiencia_id)

# Crear un nuevo rango de experiencia
@router.post("/", response_model=RangoExperienciaResponse)
def crear_rango_experiencia(rango_data: RangoExperienciaCreate, db: Session = Depends(get_db)):
    return create_rango_experiencia(db, rango_data)

# Actualizar un rango de experiencia por ID
@router.put("/{rango_experiencia_id}", response_model=RangoExperienciaResponse)
def actualizar_rango_experiencia(rango_experiencia_id: int, rango_data: RangoExperienciaUpdate, db: Session = Depends(get_db)):
    return update_rango_experiencia(db, rango_experiencia_id, rango_data)

# Eliminar un rango de experiencia por ID
@router.delete("/{rango_experiencia_id}")
def eliminar_rango_experiencia(rango_experiencia_id: int, db: Session = Depends(get_db)):
    return delete_rango_experiencia(db, rango_experiencia_id)
