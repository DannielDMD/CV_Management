from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from typing import List
#Imports de los catalogos
from app.schemas.catalogs.ciudad import CiudadCreate, CiudadResponse
from app.services.catalogs.ciudades_service import *


#Enpoint para Ciudades
router = APIRouter(
    prefix="/ciudades",
    tags=["Ciudades"]
)

@router.get("/", response_model=List[CiudadResponse])
def obtener_ciudades(db: Session = Depends(get_db)):
    return get_ciudades(db)

@router.get("/{ciudad_id}", response_model=CiudadResponse)
def obtener_ciudad(ciudad_id: int, db: Session = Depends(get_db)):
    return get_ciudad_by_id(db, ciudad_id)

@router.post("/", response_model=CiudadResponse, status_code=201)
def crear_ciudad(ciudad: CiudadCreate, db: Session = Depends(get_db)):
    return create_ciudad(db, ciudad)

@router.delete("/{ciudad_id}")
def eliminar_ciudad(ciudad_id: int, db: Session = Depends(get_db)):
    return delete_ciudad(db, ciudad_id)
