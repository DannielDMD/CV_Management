from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.catalogs.herramientas_service import (
    get_categorias_herramientas, create_categoria_herramienta, update_categoria_herramienta,
    delete_categoria_herramienta, get_herramientas, create_herramienta, update_herramienta, delete_herramienta
)
from app.schemas.herramientas import CategoriaHerramientaCreate, CategoriaHerramientaResponse, HerramientaCreate, HerramientaResponse
from app.core.database import get_db

router = APIRouter()

# Rutas para Categorías de Herramientas
@router.get("/categorias_herramientas/", response_model=list[CategoriaHerramientaResponse])
def listar_categorias_herramientas(db: Session = Depends(get_db)):
    return get_categorias_herramientas(db)

@router.post("/categorias_herramientas/", response_model=CategoriaHerramientaResponse)
def crear_categoria_herramienta(categoria: CategoriaHerramientaCreate, db: Session = Depends(get_db)):
    return create_categoria_herramienta(db, categoria)

@router.put("/categorias_herramientas/{categoria_id}", response_model=CategoriaHerramientaResponse)
def actualizar_categoria_herramienta(categoria_id: int, categoria: CategoriaHerramientaCreate, db: Session = Depends(get_db)):
    return update_categoria_herramienta(db, categoria_id, categoria)

@router.delete("/categorias_herramientas/{categoria_id}")
def eliminar_categoria_herramienta(categoria_id: int, db: Session = Depends(get_db)):
    return delete_categoria_herramienta(db, categoria_id)

# Rutas para Herramientas
@router.get("/herramientas/", response_model=list[HerramientaResponse])
def listar_herramientas(db: Session = Depends(get_db)):
    return get_herramientas(db)

@router.post("/herramientas/", response_model=HerramientaResponse)
def crear_herramienta(herramienta: HerramientaCreate, db: Session = Depends(get_db)):
    return create_herramienta(db, herramienta)

@router.put("/herramientas/{herramienta_id}", response_model=HerramientaResponse)
def actualizar_herramienta(herramienta_id: int, herramienta: HerramientaCreate, db: Session = Depends(get_db)):
    return update_herramienta(db, herramienta_id, herramienta)

@router.delete("/herramientas/{herramienta_id}")
def eliminar_herramienta(herramienta_id: int, db: Session = Depends(get_db)):
    return delete_herramienta(db, herramienta_id)
