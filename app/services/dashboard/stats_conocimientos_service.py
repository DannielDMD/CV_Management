# services/dashboard/stats_conocimientos_service.py

from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, extract

from app.models.conocimientos_model import CandidatoConocimiento, HabilidadBlanda, HabilidadTecnica, Herramienta
from app.models.candidato_model import Candidato
from app.schemas.dashboard.stats_conocimientos_schema import EstadisticasConocimientosResponse
from app.schemas.dashboard.stats_personal_schema import CountItem, MonthCountItem, MonthTopItem

def obtener_estadisticas_conocimientos(
    db: Session,
    año: Optional[int] = None
) -> EstadisticasConocimientosResponse:
    """
    Recopila estadísticas de conocimientos de los candidatos,
    opcionalmente filtradas por un año específico:
     - conocimientos_por_mes: total de registros de conocimientos cada mes del año
     - top_habilidades_blandas_anual: Top 5 habilidades blandas en todo el año
     - top_habilidades_blandas_por_mes: habilidad blanda más frecuente por mes
     - top_habilidades_tecnicas_anual: Top 5 habilidades técnicas en todo el año
     - top_habilidades_tecnicas_por_mes: habilidad técnica más frecuente por mes
     - top_herramientas_anual: Top 5 herramientas en todo el año
     - top_herramientas_por_mes: herramienta más frecuente por mes
    """

    def aplicar_filtro(query):
        if año:
            return (
                query
                .join(Candidato, CandidatoConocimiento.id_candidato == Candidato.id_candidato)
                .filter(extract("year", Candidato.fecha_registro) == año)
            )
        return query

    # 1. Conocimientos por mes
    mes_q = aplicar_filtro(
        db.query(
            extract("month", Candidato.fecha_registro).label("month"),
            func.count(CandidatoConocimiento.id_conocimiento).label("count")
        )
    ).group_by("month").order_by("month").all()
    conocimientos_por_mes = [
        MonthCountItem(month=int(r.month), count=r.count) for r in mes_q
    ]

    # 2. Top blandas anual
    blandas_anual_q = aplicar_filtro(
        db.query(
            HabilidadBlanda.nombre_habilidad_blanda.label("label"),
            func.count(CandidatoConocimiento.id_conocimiento).label("count")
        )
        .join(HabilidadBlanda, CandidatoConocimiento.id_habilidad_blanda == HabilidadBlanda.id_habilidad_blanda)
        .filter(CandidatoConocimiento.tipo_conocimiento == "blanda")
    ).group_by(HabilidadBlanda.nombre_habilidad_blanda)\
     .order_by(func.count(CandidatoConocimiento.id_conocimiento).desc())\
     .limit(5).all()
    top_habilidades_blandas_anual = [
        CountItem(label=r.label, count=r.count) for r in blandas_anual_q
    ]

    # 3. Top blandas por mes
    top_habilidades_blandas_por_mes = []
    for m in range(1, 13):
        row = aplicar_filtro(
            db.query(
                HabilidadBlanda.nombre_habilidad_blanda.label("label"),
                func.count(CandidatoConocimiento.id_conocimiento).label("count")
            )
            .join(HabilidadBlanda, CandidatoConocimiento.id_habilidad_blanda == HabilidadBlanda.id_habilidad_blanda)
            .filter(CandidatoConocimiento.tipo_conocimiento == "blanda")
        ).filter(extract("month", Candidato.fecha_registro) == m)\
         .group_by(HabilidadBlanda.nombre_habilidad_blanda)\
         .order_by(func.count(CandidatoConocimiento.id_conocimiento).desc())\
         .limit(1).first()
        if row:
            top_habilidades_blandas_por_mes.append(
                MonthTopItem(month=m, label=row.label, count=row.count)
            )

    # 4. Top técnicas anual
    tecnicas_anual_q = aplicar_filtro(
        db.query(
            HabilidadTecnica.nombre_habilidad_tecnica.label("label"),
            func.count(CandidatoConocimiento.id_conocimiento).label("count")
        )
        .join(HabilidadTecnica, CandidatoConocimiento.id_habilidad_tecnica == HabilidadTecnica.id_habilidad_tecnica)
        .filter(CandidatoConocimiento.tipo_conocimiento == "tecnica")
    ).group_by(HabilidadTecnica.nombre_habilidad_tecnica)\
     .order_by(func.count(CandidatoConocimiento.id_conocimiento).desc())\
     .limit(5).all()
    top_habilidades_tecnicas_anual = [
        CountItem(label=r.label, count=r.count) for r in tecnicas_anual_q
    ]

    # 5. Top técnicas por mes
    top_habilidades_tecnicas_por_mes = []
    for m in range(1, 13):
        row = aplicar_filtro(
            db.query(
                HabilidadTecnica.nombre_habilidad_tecnica.label("label"),
                func.count(CandidatoConocimiento.id_conocimiento).label("count")
            )
            .join(HabilidadTecnica, CandidatoConocimiento.id_habilidad_tecnica == HabilidadTecnica.id_habilidad_tecnica)
            .filter(CandidatoConocimiento.tipo_conocimiento == "tecnica")
        ).filter(extract("month", Candidato.fecha_registro) == m)\
         .group_by(HabilidadTecnica.nombre_habilidad_tecnica)\
         .order_by(func.count(CandidatoConocimiento.id_conocimiento).desc())\
         .limit(1).first()
        if row:
            top_habilidades_tecnicas_por_mes.append(
                MonthTopItem(month=m, label=row.label, count=row.count)
            )

    # 6. Top herramientas anual
    herr_anual_q = aplicar_filtro(
        db.query(
            Herramienta.nombre_herramienta.label("label"),
            func.count(CandidatoConocimiento.id_conocimiento).label("count")
        )
        .join(Herramienta, CandidatoConocimiento.id_herramienta == Herramienta.id_herramienta)
        .filter(CandidatoConocimiento.tipo_conocimiento == "herramienta")
    ).group_by(Herramienta.nombre_herramienta)\
     .order_by(func.count(CandidatoConocimiento.id_conocimiento).desc())\
     .limit(5).all()
    top_herramientas_anual = [
        CountItem(label=r.label, count=r.count) for r in herr_anual_q
    ]

    # 7. Top herramientas por mes
    top_herramientas_por_mes = []
    for m in range(1, 13):
        row = aplicar_filtro(
            db.query(
                Herramienta.nombre_herramienta.label("label"),
                func.count(CandidatoConocimiento.id_conocimiento).label("count")
            )
            .join(Herramienta, CandidatoConocimiento.id_herramienta == Herramienta.id_herramienta)
            .filter(CandidatoConocimiento.tipo_conocimiento == "herramienta")
        ).filter(extract("month", Candidato.fecha_registro) == m)\
         .group_by(Herramienta.nombre_herramienta)\
         .order_by(func.count(CandidatoConocimiento.id_conocimiento).desc())\
         .limit(1).first()
        if row:
            top_herramientas_por_mes.append(
                MonthTopItem(month=m, label=row.label, count=row.count)
            )

    return EstadisticasConocimientosResponse(
        conocimientos_por_mes=conocimientos_por_mes,
        top_habilidades_blandas_anual=top_habilidades_blandas_anual,
        top_habilidades_blandas_por_mes=top_habilidades_blandas_por_mes,
        top_habilidades_tecnicas_anual=top_habilidades_tecnicas_anual,
        top_habilidades_tecnicas_por_mes=top_habilidades_tecnicas_por_mes,
        top_herramientas_anual=top_herramientas_anual,
        top_herramientas_por_mes=top_herramientas_por_mes,
    )
