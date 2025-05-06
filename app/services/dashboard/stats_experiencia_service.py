# services/dashboard/stats_experiencia_service.py

from typing import Optional
from datetime import date

from sqlalchemy.orm import Session
from sqlalchemy import func, extract

from app.models.experiencia_model import ExperienciaLaboral
from app.models.catalogs.rango_experiencia import RangoExperiencia
from app.models.candidato_model import Candidato
from app.schemas.dashboard.stats_experiencia_schema import (
    EstadisticasExperienciaResponse
)
from app.schemas.dashboard.stats_personal_schema import (
    CountItem, MonthCountItem, MonthTopItem
)

def obtener_estadisticas_experiencia(
    db: Session,
    año: Optional[int] = None
) -> EstadisticasExperienciaResponse:
    """
    Recopila estadísticas de experiencia laboral de los candidatos,
    opcionalmente filtradas por un año específico:
      - experiencias_por_mes: total de registros cada mes del año
      - top_rangos_experiencia_anual: Top rangos en todo el año
      - top_rangos_por_mes: rango más frecuente por mes
      - top_ultimos_cargos_anual: Top cargos en todo el año
      - top_ultimos_cargos_por_mes: cargo más frecuente por mes
      - top_ultimas_empresas_anual: Top empresas en todo el año
      - top_ultimas_empresas_por_mes: empresa más frecuente por mes
      - distribucion_duracion: distribución de duración de la experiencia (filtro de año si aplica)
    """

    # Función para aplicar filtro de año sobre Candidato.fecha_registro
    def aplicar_filtro_año(query):
        if año:
            return (
                query
                .join(Candidato, ExperienciaLaboral.id_candidato == Candidato.id_candidato)
                .filter(extract("year", Candidato.fecha_registro) == año)
            )
        return query

    # 1. Experiencias por mes
    exp_mes_q = (
        aplicar_filtro_año(
            db.query(
                extract("month", Candidato.fecha_registro).label("month"),
                func.count(ExperienciaLaboral.id_experiencia).label("count")
            )
        )
        .group_by("month")
        .order_by("month")
        .all()
    )
    experiencias_por_mes = [
        MonthCountItem(month=int(r.month), count=r.count) for r in exp_mes_q
    ]

    # 2. Top rangos de experiencia anual
    rangos_anual_q = (
        aplicar_filtro_año(
            db.query(
                RangoExperiencia.descripcion_rango.label("label"),
                func.count(ExperienciaLaboral.id_experiencia).label("count")
            )
            .join(ExperienciaLaboral, ExperienciaLaboral.id_rango_experiencia == RangoExperiencia.id_rango_experiencia)
        )
        .group_by(RangoExperiencia.descripcion_rango)
        .order_by(func.count(ExperienciaLaboral.id_experiencia).desc())
        .all()
    )
    top_rangos_experiencia_anual = [
        CountItem(label=r.label, count=r.count) for r in rangos_anual_q
    ]

    # 3. Top rangos por mes
    top_rangos_por_mes = []
    for m in range(1, 13):
        row = (
            aplicar_filtro_año(
                db.query(
                    RangoExperiencia.descripcion_rango.label("label"),
                    func.count(ExperienciaLaboral.id_experiencia).label("count")
                )
                .join(ExperienciaLaboral, ExperienciaLaboral.id_rango_experiencia == RangoExperiencia.id_rango_experiencia)
            )
            .filter(extract("month", Candidato.fecha_registro) == m)
            .group_by(RangoExperiencia.descripcion_rango)
            .order_by(func.count(ExperienciaLaboral.id_experiencia).desc())
            .limit(1)
            .first()
        )
        if row:
            top_rangos_por_mes.append(
                MonthTopItem(month=m, label=row.label, count=row.count)
            )

    # 4. Top últimos cargos anual
    cargos_anual_q = (
        aplicar_filtro_año(
            db.query(
                ExperienciaLaboral.ultimo_cargo.label("label"),
                func.count(ExperienciaLaboral.id_experiencia).label("count")
            )
        )
        .group_by(ExperienciaLaboral.ultimo_cargo)
        .order_by(func.count(ExperienciaLaboral.id_experiencia).desc())
        .limit(5)
        .all()
    )
    top_ultimos_cargos_anual = [
        CountItem(label=c.label, count=c.count) for c in cargos_anual_q
    ]

    # 5. Top últimos cargos por mes
    top_ultimos_cargos_por_mes = []
    for m in range(1, 13):
        row = (
            aplicar_filtro_año(
                db.query(
                    ExperienciaLaboral.ultimo_cargo.label("label"),
                    func.count(ExperienciaLaboral.id_experiencia).label("count")
                )
            )
            .filter(extract("month", Candidato.fecha_registro) == m)
            .group_by(ExperienciaLaboral.ultimo_cargo)
            .order_by(func.count(ExperienciaLaboral.id_experiencia).desc())
            .limit(1)
            .first()
        )
        if row:
            top_ultimos_cargos_por_mes.append(
                MonthTopItem(month=m, label=row.label, count=row.count)
            )

    # 6. Top últimas empresas anual
    empresas_anual_q = (
        aplicar_filtro_año(
            db.query(
                ExperienciaLaboral.ultima_empresa.label("label"),
                func.count(ExperienciaLaboral.id_experiencia).label("count")
            )
        )
        .group_by(ExperienciaLaboral.ultima_empresa)
        .order_by(func.count(ExperienciaLaboral.id_experiencia).desc())
        .limit(5)
        .all()
    )
    top_ultimas_empresas_anual = [
        CountItem(label=e.label, count=e.count) for e in empresas_anual_q
    ]

    # 7. Top últimas empresas por mes
    top_ultimas_empresas_por_mes = []
    for m in range(1, 13):
        row = (
            aplicar_filtro_año(
                db.query(
                    ExperienciaLaboral.ultima_empresa.label("label"),
                    func.count(ExperienciaLaboral.id_experiencia).label("count")
                )
            )
            .filter(extract("month", Candidato.fecha_registro) == m)
            .group_by(ExperienciaLaboral.ultima_empresa)
            .order_by(func.count(ExperienciaLaboral.id_experiencia).desc())
            .limit(1)
            .first()
        )
        if row:
            top_ultimas_empresas_por_mes.append(
                MonthTopItem(month=m, label=row.label, count=row.count)
            )

    # 8. Distribución de duración (filtrada por año si aplica)
    sesiones = aplicar_filtro_año(
        db.query(
            ExperienciaLaboral.fecha_inicio,
            ExperienciaLaboral.fecha_fin
        )
    ).all()
    today = date.today()
    duraciones = []
    for inicio, fin in sesiones:
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
        CountItem(label=k, count=v) for k, v in buckets.items()
    ]

    return EstadisticasExperienciaResponse(
        experiencias_por_mes=experiencias_por_mes,
        top_rangos_experiencia_anual=top_rangos_experiencia_anual,
        top_rangos_por_mes=top_rangos_por_mes,
        top_ultimos_cargos_anual=top_ultimos_cargos_anual,
        top_ultimos_cargos_por_mes=top_ultimos_cargos_por_mes,
        top_ultimas_empresas_anual=top_ultimas_empresas_anual,
        top_ultimas_empresas_por_mes=top_ultimas_empresas_por_mes,
        distribucion_duracion=distribucion_duracion
    )
