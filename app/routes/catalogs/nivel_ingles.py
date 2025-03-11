from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.catalogs.nivel_ingles_service import (
    get_niveles_ingles, get_nivel_ingles, create_nivel_ingles,
    update_nivel_ingles, delete_nivel_ingles
)
from app.schemas.catalogs.nivel_ingles import NivelInglesResponse, NivelInglesCreate, NivelInglesUpdate
from typing import List

router = APIRouter(prefix="/nivel-ingles", tags=["Nivel de Inglés"])

# Obtener todos los niveles de inglés
@router.get("/", response_model=List[NivelInglesResponse])
def listar_niveles_ingles(db: Session = Depends(get_db)):
    return get_niveles_ingles(db)

# Obtener un nivel de inglés por ID
@router.get("/{nivel_ingles_id}", response_model=NivelInglesResponse)
def obtener_nivel_ingles(nivel_ingles_id: int, db: Session = Depends(get_db)):
    return get_nivel_ingles(db, nivel_ingles_id)

# Crear un nuevo nivel de inglés
@router.post("/", response_model=NivelInglesResponse)
def crear_nivel_ingles(nivel_ingles_data: NivelInglesCreate, db: Session = Depends(get_db)):
    return create_nivel_ingles(db, nivel_ingles_data)

# Actualizar un nivel de inglés por ID
@router.put("/{nivel_ingles_id}", response_model=NivelInglesResponse)
def actualizar_nivel_ingles(nivel_ingles_id: int, nivel_ingles_data: NivelInglesUpdate, db: Session = Depends(get_db)):
    return update_nivel_ingles(db, nivel_ingles_id, nivel_ingles_data)

# Eliminar un nivel de inglés por ID
@router.delete("/{nivel_ingles_id}")
def eliminar_nivel_ingles(nivel_ingles_id: int, db: Session = Depends(get_db)):
    return delete_nivel_ingles(db, nivel_ingles_id)
