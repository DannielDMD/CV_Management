# services/dashboard/stats_experiencia_service.py

from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date


from app.models.catalogs.rango_experiencia import RangoExperiencia
from app.models.experiencia_model import ExperienciaLaboral
from app.schemas.dashboard.stats_experiencia_schema import EstadisticasExperienciaResponse
from app.schemas.dashboard.stats_personal_schema import CountItem

def obtener_estadisticas_experiencia(db: Session) -> EstadisticasExperienciaResponse:
    """
    Recopila estadísticas de experiencia laboral de los candidatos:
     - Top rangos de experiencia
     - Top 5 últimos cargos
     - Top 5 últimas empresas
     - Distribución de duración de la experiencia
    """

    # 1. Top rangos de experiencia
    rangos_query = (
        db.query(
            RangoExperiencia.descripcion_rango.label("label"),
            func.count(ExperienciaLaboral.id_experiencia).label("count")
        )
        .join(ExperienciaLaboral, ExperienciaLaboral.id_rango_experiencia == RangoExperiencia.id_rango_experiencia)
        .group_by(RangoExperiencia.descripcion_rango)
        .order_by(func.count(ExperienciaLaboral.id_experiencia).desc())
        .all()
    )
    top_rangos_experiencia = [
        CountItem(label=r.label, count=r.count) for r in rangos_query
    ]

    # 2. Top 5 últimos cargos
    cargos_query = (
        db.query(
            ExperienciaLaboral.ultimo_cargo.label("label"),
            func.count(ExperienciaLaboral.id_experiencia).label("count")
        )
        .group_by(ExperienciaLaboral.ultimo_cargo)
        .order_by(func.count(ExperienciaLaboral.id_experiencia).desc())
        .limit(5)
        .all()
    )
    top_ultimos_cargos = [
        CountItem(label=c.label, count=c.count) for c in cargos_query
    ]

    # 3. Top 5 últimas empresas
    empresas_query = (
        db.query(
            ExperienciaLaboral.ultima_empresa.label("label"),
            func.count(ExperienciaLaboral.id_experiencia).label("count")
        )
        .group_by(ExperienciaLaboral.ultima_empresa)
        .order_by(func.count(ExperienciaLaboral.id_experiencia).desc())
        .limit(5)
        .all()
    )
    top_ultimas_empresas = [
        CountItem(label=e.label, count=e.count) for e in empresas_query
    ]

    # 4. Distribución de duración de la experiencia
    experiencias = db.query(
        ExperienciaLaboral.fecha_inicio,
        ExperienciaLaboral.fecha_fin
    ).all()
    today = date.today()
    duraciones = []
    for inicio, fin in experiencias:
        end_date = fin or today
        years = (end_date - inicio).days / 365.0
        duraciones.append(years)

    buckets = {"<1 año": 0, "1-3 años": 0, "3-5 años": 0, "Más de 5 años": 0}
    for yrs in duraciones:
        if yrs < 1:
            buckets["<1 año"] += 1
        elif yrs < 3:
            buckets["1-3 años"] += 1
        elif yrs < 5:
            buckets["3-5 años"] += 1
        else:
            buckets["Más de 5 años"] += 1
    distribucion_duracion = [
        CountItem(label=label, count=count) for label, count in buckets.items()
    ]

    return EstadisticasExperienciaResponse(
        top_rangos_experiencia=top_rangos_experiencia,
        top_ultimos_cargos=top_ultimos_cargos,
        top_ultimas_empresas=top_ultimas_empresas,
        distribucion_duracion=distribucion_duracion
    )
