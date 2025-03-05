from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.herramientas_service import (
    obtener_categorias_herramientas,
    obtener_herramientas_por_categoria,
    obtener_herramientas_candidato,
    asignar_herramienta_a_candidato,
    eliminar_herramienta_de_candidato
)
from app.schemas.herramientas import HerramientaCandidatoCreate, HerramientaCandidatoResponse

router = APIRouter(prefix="/herramientas", tags=["Herramientas"])

# Obtener todas las categorías de herramientas
@router.get("/categorias")
def listar_categorias(db: Session = Depends(get_db)):
    return obtener_categorias_herramientas(db)

# Obtener herramientas por categoría
@router.get("/categoria/{id_categoria}")
def listar_herramientas_por_categoria(id_categoria: int, db: Session = Depends(get_db)):
    return obtener_herramientas_por_categoria(db, id_categoria)

@router.get("/candidato/{id_candidato}", response_model=list[HerramientaCandidatoResponse])
def obtener_herramientas_por_candidato(id_candidato: int, db: Session = Depends(get_db)):
    return obtener_herramientas_candidato(db, id_candidato)

# Asignar una herramienta a un candidato
@router.post("/asignar")
def asignar_herramienta(herramienta_data: HerramientaCandidatoCreate, db: Session = Depends(get_db)):
    return asignar_herramienta_a_candidato(db, herramienta_data)

# Eliminar una herramienta de un candidato
@router.delete("/eliminar/{id_candidato}/{id_herramienta}")
def eliminar_herramienta(id_candidato: int, id_herramienta: int, db: Session = Depends(get_db)):
    return eliminar_herramienta_de_candidato(db, id_candidato, id_herramienta)
