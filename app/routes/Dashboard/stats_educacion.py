# routes/Dashboard/stats_educacion.py


from typing import Optional
from fastapi import APIRouter, Depends, Query
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
    summary="Obtener estadísticas de educación de los candidatos filtradas por año"
)
def estadisticas_educacion(
    año: Optional[int] = Query(
        None,
        title="Año",
        description="Año para filtrar las estadísticas de educación (por ejemplo, 2025). Si no se indica, usa todos los años."
    ),
    db: Session = Depends(get_db)
):
    """
    Devuelve un objeto con:
    - educaciones_por_mes: total de registros de educación cada mes del año indicado
    - top_niveles_educacion_anual: Top 5 niveles educativos en el año
    - top_niveles_por_mes: nivel más frecuente por mes
    - top_titulos_obtenidos_anual: Top 5 títulos en el año
    - top_titulos_por_mes: título más frecuente por mes
    - top_instituciones_academicas_anual: Top 5 instituciones en el año
    - top_instituciones_por_mes: institución más frecuente por mes
    - distribucion_nivel_ingles_anual: distribución de nivel de inglés en el año
    - distribucion_nivel_ingles_por_mes: nivel de inglés más frecuente por mes
    - distribucion_anio_graduacion: conteo por año de graduación (sin filtro de año)
    """
    return obtener_estadisticas_educacion(db, año)




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
