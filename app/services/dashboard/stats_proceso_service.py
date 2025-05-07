# services/dashboard/stats_proceso_service.py

from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, extract

from app.models.candidato_model import Candidato
from app.schemas.dashboard.stats_proceso_schema import EstadisticasProcesoResponse
from app.schemas.dashboard.stats_personal_schema import CountItem, MonthCountItem, MonthTopItem

def obtener_estadisticas_proceso(
    db: Session,
    año: Optional[int] = None
) -> EstadisticasProcesoResponse:
    """
    Recopila estadísticas del proceso de selección de los candidatos,
    opcionalmente filtradas por un año específico:
     - candidatos_por_mes: total de registros por mes
     - top_estados_anual: conteo por estado en todo el año
     - top_estados_por_mes: estado más frecuente en cada mes del año
    """

    # Aplica filtro de año si se proporciona
    def aplicar_filtro(query):
        if año:
            return query.filter(extract("year", Candidato.fecha_registro) == año)
        return query

    # 1. Candidatos por mes
    mes_q = (
        aplicar_filtro(
            db.query(
                extract("month", Candidato.fecha_registro).label("month"),
                func.count(Candidato.id_candidato).label("count"),
            )
        )
        .group_by("month")
        .order_by("month")
        .all()
    )
    candidatos_por_mes = [
        MonthCountItem(month=int(r.month), count=r.count) for r in mes_q
    ]

    # 2. Top estados anual
    anual_q = (
        aplicar_filtro(
            db.query(
                Candidato.estado.label("label"),
                func.count(Candidato.id_candidato).label("count"),
            )
        )
        .group_by(Candidato.estado)
        .order_by(func.count(Candidato.id_candidato).desc())
        .all()
    )
    top_estados_anual = [CountItem(label=r.label, count=r.count) for r in anual_q]

    # 3. Top estado por mes
    top_estados_por_mes = []
    for m in range(1, 13):
        row = (
            aplicar_filtro(
                db.query(
                    Candidato.estado.label("label"),
                    func.count(Candidato.id_candidato).label("count"),
                )
            )
            .filter(extract("month", Candidato.fecha_registro) == m)
            .group_by(Candidato.estado)
            .order_by(func.count(Candidato.id_candidato).desc())
            .limit(1)
            .first()
        )
        if row:
            top_estados_por_mes.append(
                MonthTopItem(month=m, label=row.label, count=row.count)
            )

    return EstadisticasProcesoResponse(
        candidatos_por_mes=candidatos_por_mes,
        top_estados_anual=top_estados_anual,
        top_estados_por_mes=top_estados_por_mes,
    )
