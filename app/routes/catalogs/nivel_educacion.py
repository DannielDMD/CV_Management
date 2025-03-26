from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.catalogs.nivel_educacion_service import (
    get_niveles_educacion, 
    get_nivel_educacion, 
    create_nivel_educacion, 
    update_nivel_educacion, 
    delete_nivel_educacion
)
from app.schemas.catalogs.nivel_educacion import NivelEducacionCreate, NivelEducacionUpdate, NivelEducacionResponse
from app.core.database import get_db

router = APIRouter(prefix="/nivel-educacion", tags=["Nivel Educación"])

# Obtener todos los niveles de educación
@router.get("/", response_model=list[NivelEducacionResponse])
def listar_niveles_educacion(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_niveles_educacion(db, skip, limit)

# Obtener un nivel de educación por ID
@router.get("/{id_nivel_educacion}", response_model=NivelEducacionResponse)
def obtener_nivel_educacion(id_nivel_educacion: int, db: Session = Depends(get_db)):
    nivel = get_nivel_educacion(db, id_nivel_educacion)
    if not nivel:
        raise HTTPException(status_code=404, detail="Nivel de educación no encontrado")
    return nivel

# Crear un nuevo nivel de educación
@router.post("/", response_model=NivelEducacionResponse)
def crear_nivel_educacion(nivel_educacion_data: NivelEducacionCreate, db: Session = Depends(get_db)):
    return create_nivel_educacion(db, nivel_educacion_data)

# Actualizar un nivel de educación existente
@router.put("/{id_nivel_educacion}", response_model=NivelEducacionResponse)
def actualizar_nivel_educacion(id_nivel_educacion: int, nivel_educacion_data: NivelEducacionUpdate, db: Session = Depends(get_db)):
    nivel_actualizado = update_nivel_educacion(db, id_nivel_educacion, nivel_educacion_data)
    if not nivel_actualizado:
        raise HTTPException(status_code=404, detail="Nivel de educación no encontrado")
    return nivel_actualizado

# Eliminar un nivel de educación
@router.delete("/{id_nivel_educacion}", response_model=NivelEducacionResponse)
def eliminar_nivel_educacion(id_nivel_educacion: int, db: Session = Depends(get_db)):
    nivel_eliminado = delete_nivel_educacion(db, id_nivel_educacion)
    if not nivel_eliminado:
        raise HTTPException(status_code=404, detail="Nivel de educación no encontrado")
    return nivel_eliminado
