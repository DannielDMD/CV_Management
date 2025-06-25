"""Rutas para la gestión de candidatos, incluyendo creación, actualización, consulta, eliminación y estadísticas."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.dashboard.stats_general_service import obtener_estadisticas_generales


router = APIRouter(
    prefix="/dashboard/stats",
    tags=["Dashboard General"]
)

@router.get("/general")
def get_general_stats(
    db: Session = Depends(get_db),
    anio: int = Query(None, description="Año opcional para filtrar las estadísticas")
):
    return obtener_estadisticas_generales(db, anio)