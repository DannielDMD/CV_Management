from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.catalogs.conocimientos_service import (
    get_habilidades_blandas,
    get_habilidades_tecnicas,
    get_herramientas
)
from app.core.database import get_db
from app.schemas.catalogs.conocimientos_schema import HabilidadBlandaResponse, HabilidadTecnicaResponse, HerramientaResponse

router = APIRouter(prefix="/conocimientos", tags=["Conocimientos"])

@router.get("/habilidades-blandas", response_model=list[HabilidadBlandaResponse])
def obtener_habilidades_blandas(db: Session = Depends(get_db)):
    return get_habilidades_blandas(db)

@router.get("/habilidades-tecnicas", response_model=list[HabilidadTecnicaResponse])
def obtener_habilidades_tecnicas(db: Session = Depends(get_db)):
    return get_habilidades_tecnicas(db)

@router.get("/herramientas", response_model=list[HerramientaResponse])
def obtener_herramientas(db: Session = Depends(get_db)):
    return get_herramientas(db)
