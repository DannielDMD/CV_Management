# app/routes/Dashboard/stats_routes.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.dashboard.stats_service import obtener_anios_disponibles

router = APIRouter(
    prefix="/reportes",
    tags=["Reportes – Años disponibles"]
)

@router.get("/anios-disponibles", response_model=list[int])
def anios_disponibles(db: Session = Depends(get_db)):
    """
    Devuelve los años disponibles con registros de candidatos (basado en fecha_registro).

    Returns:
        List[int]: Años únicos donde hay registros.
    """
    return obtener_anios_disponibles(db)
