"""Rutas para la gestión de departamentos."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.schemas.catalogs.ciudad import (
    DepartamentoCreate,
    DepartamentoPaginatedResponse,
    DepartamentoResponse,
)
from app.services.catalogs.departamentos_service import (
    crear_departamento,
    get_departamentos_con_paginacion,
    obtener_departamento_por_id,
    actualizar_departamento,
    eliminar_departamento,
    obtener_todos_departamentos,
)
from app.core.database import get_db

router = APIRouter(prefix="/departamentos", tags=["Departamentos"])

@router.get("/todas", response_model=List[DepartamentoResponse])
def listar_departamentos(db: Session = Depends(get_db)):
    return obtener_todos_departamentos(db)


@router.post("/", response_model=DepartamentoResponse, status_code=status.HTTP_201_CREATED)
def crear_nuevo_departamento(data: DepartamentoCreate, db: Session = Depends(get_db)):
    departamento = crear_departamento(db, data)
    if not departamento:
        raise HTTPException(status_code=400, detail="Ya existe un departamento con ese nombre")
    return departamento


@router.get("/", response_model=DepartamentoPaginatedResponse)
def listar_departamentos_con_paginacion(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Lista de departamentos con paginación y búsqueda opcional por nombre.
    """
    return get_departamentos_con_paginacion(
        db=db,
        skip=skip,
        limit=limit,
        search=search
    )


@router.get("/{id_departamento}", response_model=DepartamentoResponse)
def obtener_departamento(id_departamento: int, db: Session = Depends(get_db)):
    departamento = obtener_departamento_por_id(db, id_departamento)
    if not departamento:
        raise HTTPException(status_code=404, detail="Departamento no encontrado")
    return departamento


@router.put("/{id_departamento}", response_model=DepartamentoResponse)
def actualizar_departamento_por_id(id_departamento: int, data: DepartamentoCreate, db: Session = Depends(get_db)):
    actualizado = actualizar_departamento(db, id_departamento, data)
    if not actualizado:
        raise HTTPException(status_code=400, detail="Ya existe otro departamento con ese nombre o no se encontró el registro")
    return actualizado


@router.delete("/{id_departamento}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_departamento_por_id(id_departamento: int, db: Session = Depends(get_db)):
    eliminado = eliminar_departamento(db, id_departamento)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Departamento no encontrado o no se pudo eliminar por relaciones existentes")
    return
