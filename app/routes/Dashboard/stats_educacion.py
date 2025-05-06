# routes/Dashboard/stats_educacion.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.dashboard.stats_educacion_service import obtener_estadisticas_educacion
from app.schemas.dashboard.stats_educacion_schema import EstadisticasEducacionResponse

router = APIRouter(
    prefix="/reportes/educacion",
    tags=["Reportes – Educación"]
)

@router.get(
    "/",
    response_model=EstadisticasEducacionResponse,
    summary="Obtener estadísticas de educación de los candidatos"
)
def estadisticas_educacion(db: Session = Depends(get_db)):
    """
    Devuelve:
    - Top 5 niveles educativos
    - Top 5 títulos obtenidos
    - Top 5 instituciones académicas
    - Distribución por nivel de inglés
    - Distribución por año de graduación
    """
    return obtener_estadisticas_educacion(db)




"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.models.educacion_model import Educacion
from app.models.catalogs.nivel_educacion import NivelEducacion

router = APIRouter(prefix="/dashboard/stats", tags=["Estadísticas Educación"])

@router.get("/educacion")
def get_educational_distribution(db: Session = Depends(get_db)):
    resultados = (
        db.query(NivelEducacion.descripcion_nivel, func.count(Educacion.id_educacion).label("total"))
        .join(Educacion, Educacion.id_nivel_educacion == NivelEducacion.id_nivel_educacion)
        .group_by(NivelEducacion.descripcion_nivel)
        .order_by(func.count(Educacion.id_educacion).desc())
        .all()
    )

    return [{"nivel": descripcion, "total": total} for descripcion, total in resultados]"""
