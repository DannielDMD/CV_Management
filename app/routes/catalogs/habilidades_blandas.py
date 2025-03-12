from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.catalogs.habilidades_blandas_service import (
    get_all_habilidades_blandas,
    get_habilidad_blanda,
    create_habilidad_blanda,
    update_habilidad_blanda,
    delete_habilidad_blanda
)
from app.schemas.habilidades_blandas import HabilidadBlandaCreate, HabilidadBlandaUpdate, HabilidadBlandaResponse
from app.core.database import get_db

router = APIRouter(prefix="/habilidades-blandas", tags=["Habilidades Blandas"])

# Obtener todas las habilidades blandas
@router.get("/", response_model=list[HabilidadBlandaResponse])
def get_all(db: Session = Depends(get_db)):
    return get_all_habilidades_blandas(db)

# Obtener una habilidad blanda por ID
@router.get("/{id_habilidad_blanda}", response_model=HabilidadBlandaResponse)
def get_by_id(id_habilidad_blanda: int, db: Session = Depends(get_db)):
    return get_habilidad_blanda(db, id_habilidad_blanda)

# Crear una nueva habilidad blanda
@router.post("/", response_model=HabilidadBlandaResponse)
def create(habilidad_data: HabilidadBlandaCreate, db: Session = Depends(get_db)):
    return create_habilidad_blanda(db, habilidad_data)

# Actualizar una habilidad blanda
@router.put("/{id_habilidad_blanda}", response_model=HabilidadBlandaResponse)
def update(id_habilidad_blanda: int, habilidad_data: HabilidadBlandaUpdate, db: Session = Depends(get_db)):
    return update_habilidad_blanda(db, id_habilidad_blanda, habilidad_data)

# Eliminar una habilidad blanda
@router.delete("/{id_habilidad_blanda}")
def delete(id_habilidad_blanda: int, db: Session = Depends(get_db)):
    return delete_habilidad_blanda(db, id_habilidad_blanda)
