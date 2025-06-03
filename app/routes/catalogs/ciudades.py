"""Rutas para la gestión del catálogo de ciudades."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.catalogs.ciudad import CiudadCreate, CiudadResponse
from app.services.catalogs.ciudades_service import (
    get_ciudades,
    get_ciudad_by_id,
    get_ciudades_por_departamento,
    create_ciudad,
    delete_ciudad,
)
from app.core.database import get_db

router = APIRouter(prefix="/ciudades", tags=["Ciudades"])


@router.get("/", response_model=List[CiudadResponse])
def listar_ciudades(db: Session = Depends(get_db)):
    return get_ciudades(db)


@router.get("/{ciudad_id}", response_model=CiudadResponse)
def obtener_ciudad(ciudad_id: int, db: Session = Depends(get_db)):
    ciudad = get_ciudad_by_id(db, ciudad_id)
    if not ciudad:
        raise HTTPException(status_code=404, detail="Ciudad no encontrada")
    return ciudad


@router.get("/departamento/{id_departamento}", response_model=List[CiudadResponse])
def listar_ciudades_por_departamento(id_departamento: int, db: Session = Depends(get_db)):
    return get_ciudades_por_departamento(db, id_departamento)


@router.post("/", response_model=CiudadResponse, status_code=status.HTTP_201_CREATED)
def crear_nueva_ciudad(ciudad_data: CiudadCreate, db: Session = Depends(get_db)):
    ciudad = create_ciudad(db, ciudad_data)
    if not ciudad:
        raise HTTPException(status_code=400, detail="Ya existe una ciudad con ese nombre en ese departamento")
    return ciudad


@router.delete("/{ciudad_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_ciudad(ciudad_id: int, db: Session = Depends(get_db)):
    eliminada = delete_ciudad(db, ciudad_id)
    if not eliminada:
        raise HTTPException(status_code=404, detail="Ciudad no encontrada o no se puede eliminar")
    return
