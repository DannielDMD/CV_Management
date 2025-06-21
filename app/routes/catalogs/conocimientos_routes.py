"""Rutas para consultar los catálogos de conocimientos (habilidades y herramientas)."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.services.catalogs.conocimientos_service import (
    create_habilidad_blanda,
    create_habilidad_tecnica,
    create_herramienta,
    delete_habilidad_blanda,
    delete_habilidad_tecnica,
    delete_herramienta,
    get_habilidades_blandas,
    get_habilidades_blandas_con_paginacion,
    get_habilidades_tecnicas,
    get_habilidades_tecnicas_con_paginacion,
    get_herramientas,
    get_herramientas_con_paginacion,
    update_habilidad_blanda,
    update_habilidad_tecnica,
    update_herramienta
)
from app.schemas.catalogs.conocimientos_schema import (
    HabilidadBlandaCreate,
    HabilidadBlandaPaginatedResponse,
    HabilidadBlandaResponse,
    HabilidadTecnicaCreate,
    HabilidadTecnicaPaginatedResponse,
    HabilidadTecnicaResponse,
    HerramientaCreate,
    HerramientaPaginatedResponse,
    HerramientaResponse
)

router = APIRouter(prefix="/conocimientos", tags=["Conocimientos"])

# ----------------------------
# Habilidad Blanda
# ----------------------------

@router.get("/habilidades-blandas/todas", response_model=List[HabilidadBlandaResponse])
def obtener_habilidades_blandas(db: Session = Depends(get_db)):
    """
    Lista todas las habilidades blandas disponibles.

    Args:
        db (Session): Sesión de base de datos inyectada.

    Returns:
        List[HabilidadBlandaResponse]: Lista de habilidades blandas.
    """
    return get_habilidades_blandas(db)


@router.get("/habilidades-blandas", response_model=HabilidadBlandaPaginatedResponse)
def listar_habilidades_blandas(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    return get_habilidades_blandas_con_paginacion(db, skip, limit, search)




@router.post("/habilidades-blandas", response_model=HabilidadBlandaResponse, status_code=201)
def crear_habilidad_blanda(data: HabilidadBlandaCreate, db: Session = Depends(get_db)):
    return create_habilidad_blanda(db, data)


@router.put("/habilidades-blandas/{id_habilidad}", response_model=HabilidadBlandaResponse)
def actualizar_habilidad_blanda(id_habilidad: int, data: HabilidadBlandaCreate, db: Session = Depends(get_db)):
    return update_habilidad_blanda(db, id_habilidad, data)


@router.delete("/habilidades-blandas/{id_habilidad}")
def eliminar_habilidad_blanda(id_habilidad: int, db: Session = Depends(get_db)):
    if not delete_habilidad_blanda(db, id_habilidad):
        raise HTTPException(status_code=404, detail="Habilidad blanda no encontrada")
    
# ----------------------------
# Habilidad Técnica
# ----------------------------

@router.get("/habilidades-tecnicas/todas", response_model=List[HabilidadTecnicaResponse])
def obtener_habilidades_tecnicas(db: Session = Depends(get_db)):
    return get_habilidades_tecnicas(db)

@router.get("/habilidades-tecnicas", response_model=HabilidadTecnicaPaginatedResponse)
def listar_habilidades_tecnicas(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    return get_habilidades_tecnicas_con_paginacion(db, skip, limit, search)

@router.post("/habilidades-tecnicas", response_model=HabilidadTecnicaResponse, status_code=201)
def crear_habilidad_tecnica(data: HabilidadTecnicaCreate, db: Session = Depends(get_db)):
    return create_habilidad_tecnica(db, data)


@router.put("/habilidades-tecnicas/{id_habilidad}", response_model=HabilidadTecnicaResponse)
def actualizar_habilidad_tecnica(id_habilidad: int, data: HabilidadTecnicaCreate, db: Session = Depends(get_db)):
    return update_habilidad_tecnica(db, id_habilidad, data)


@router.delete("/habilidades-tecnicas/{id_habilidad}", status_code=204)
def eliminar_habilidad_tecnica(id_habilidad: int, db: Session = Depends(get_db)):
    if not delete_habilidad_tecnica(db, id_habilidad):
        raise HTTPException(status_code=404, detail="Habilidad técnica no encontrada")


# ----------------------------
# Herramienta
# ----------------------------


@router.get("/herramientas/todas", response_model=List[HerramientaResponse])
def obtener_herramientas(db: Session = Depends(get_db)):
    return get_herramientas(db)

@router.get("/herramientas", response_model=HerramientaPaginatedResponse)
def listar_herramientas(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    return get_herramientas_con_paginacion(db, skip, limit, search)

@router.post("/herramientas", response_model=HerramientaResponse, status_code=201)
def crear_herramienta(data: HerramientaCreate, db: Session = Depends(get_db)):
    return create_herramienta(db, data)


@router.put("/herramientas/{id_herramienta}", response_model=HerramientaResponse)
def actualizar_herramienta(id_herramienta: int, data: HerramientaCreate, db: Session = Depends(get_db)):
    return update_herramienta(db, id_herramienta, data)


@router.delete("/herramientas/{id_herramienta}", status_code=204)
def eliminar_herramienta(id_herramienta: int, db: Session = Depends(get_db)):
    if not delete_herramienta(db, id_herramienta):
        raise HTTPException(status_code=404, detail="Herramienta no encontrada")
