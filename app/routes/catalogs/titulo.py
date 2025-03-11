from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.catalogs.titulo import TituloObtenidoCreate, TituloObtenidoUpdate, TituloObtenidoResponse
from app.services.catalogs.titulo_service import get_titulo, get_titulos, create_titulo, update_titulo, delete_titulo

router = APIRouter(prefix="/titulos", tags=["Títulos Obtenidos"])

@router.get("/", response_model=list[TituloObtenidoResponse])
def read_titulos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_titulos(db, skip, limit)

@router.get("/{titulo_id}", response_model=TituloObtenidoResponse)
def read_titulo(titulo_id: int, db: Session = Depends(get_db)):
    return get_titulo(db, titulo_id)

@router.post("/", response_model=TituloObtenidoResponse, status_code=201)
def create_titulo_endpoint(titulo: TituloObtenidoCreate, db: Session = Depends(get_db)):
    return create_titulo(db, titulo)

@router.put("/{titulo_id}", response_model=TituloObtenidoResponse)
def update_titulo_endpoint(titulo_id: int, titulo_update: TituloObtenidoUpdate, db: Session = Depends(get_db)):
    return update_titulo(db, titulo_id, titulo_update)

@router.delete("/{titulo_id}")
def delete_titulo_endpoint(titulo_id: int, db: Session = Depends(get_db)):
    return delete_titulo(db, titulo_id)
