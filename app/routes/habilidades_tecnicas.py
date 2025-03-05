from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.habilidades_tecnicas_service import (
    get_all_categorias_habilidades_tecnicas,
    get_all_habilidades_tecnicas,
    assign_habilidad_tecnica,
    get_habilidades_tecnicas_by_candidato,
    remove_habilidad_tecnica
)
from app.schemas.habilidades_tecnicas import HabilidadTecnicaCandidatoCreate

router = APIRouter(prefix="/habilidades-tecnicas", tags=["Habilidades Técnicas"])

@router.get("/categorias")
def obtener_categorias(db: Session = Depends(get_db)):
    return get_all_categorias_habilidades_tecnicas(db)

@router.get("/")
def obtener_habilidades(db: Session = Depends(get_db)):
    return get_all_habilidades_tecnicas(db)

@router.post("/asignar")
def asignar_habilidad(habilidad_data: HabilidadTecnicaCandidatoCreate, db: Session = Depends(get_db)):
    return assign_habilidad_tecnica(db, habilidad_data)

@router.get("/candidato/{id_candidato}")
def obtener_habilidades_candidato(id_candidato: int, db: Session = Depends(get_db)):
    return get_habilidades_tecnicas_by_candidato(db, id_candidato)

@router.delete("/eliminar/{id_candidato}/{id_habilidad}")
def eliminar_habilidad(id_candidato: int, id_habilidad: int, db: Session = Depends(get_db)):
    return remove_habilidad_tecnica(db, id_candidato, id_habilidad)
