from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from typing import List
#Imports de los catalogos
from app.schemas.catalogs.cargo_ofrecido import *
from app.services.catalogs.cargos_ofrecidos_service import *

# Cargos asociados a las categorias
router = APIRouter(prefix="/cargo-ofrecido", tags=["Cargo Ofrecido"])

@router.post("/", response_model=CargoOfrecidoResponse)
def crear_cargo(cargo_data: CargoOfrecidoCreate, db: Session = Depends(get_db)):
    return crear_cargo_ofrecido(db, cargo_data)

@router.get("/", response_model=list[CargoOfrecidoResponse])
def listar_cargos(db: Session = Depends(get_db)):
    return obtener_cargos_ofrecidos(db)

@router.get("/{id_cargo}", response_model=CargoOfrecidoResponse)
def obtener_cargo(id_cargo: int, db: Session = Depends(get_db)):
    return obtener_cargo_ofrecido_por_id(db, id_cargo)


@router.delete("/{id_cargo}")
def eliminar_cargo(id_cargo: int, db: Session = Depends(get_db)):
    return eliminar_cargo_ofrecido(db, id_cargo)