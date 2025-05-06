# services/dashboard/stats_conocimientos_service.py

from sqlalchemy.orm import Session
from sqlalchemy import func



from app.models.conocimientos_model import CandidatoConocimiento, HabilidadBlanda, HabilidadTecnica, Herramienta
from app.schemas.dashboard.stats_conocimientos_schema import EstadisticasConocimientosResponse
from app.schemas.dashboard.stats_personal_schema import CountItem

def obtener_estadisticas_conocimientos(db: Session) -> EstadisticasConocimientosResponse:
    """
    Recopila estadísticas de conocimientos de los candidatos:
     - Top 5 habilidades blandas
     - Top 5 habilidades técnicas
     - Top 5 herramientas
    """

    # 1. Top 5 habilidades blandas
    blandas_query = (
        db.query(
            HabilidadBlanda.nombre_habilidad_blanda.label("label"),
            func.count(CandidatoConocimiento.id_conocimiento).label("count")
        )
        .join(HabilidadBlanda,
              CandidatoConocimiento.id_habilidad_blanda == HabilidadBlanda.id_habilidad_blanda)
        .filter(CandidatoConocimiento.tipo_conocimiento == 'blanda')
        .group_by(HabilidadBlanda.nombre_habilidad_blanda)
        .order_by(func.count(CandidatoConocimiento.id_conocimiento).desc())
        .limit(5)
        .all()
    )
    top_habilidades_blandas = [
        CountItem(label=h.label, count=h.count) for h in blandas_query
    ]

    # 2. Top 5 habilidades técnicas
    tecnicas_query = (
        db.query(
            HabilidadTecnica.nombre_habilidad_tecnica.label("label"),
            func.count(CandidatoConocimiento.id_conocimiento).label("count")
        )
        .join(HabilidadTecnica,
              CandidatoConocimiento.id_habilidad_tecnica == HabilidadTecnica.id_habilidad_tecnica)
        .filter(CandidatoConocimiento.tipo_conocimiento == 'tecnica')
        .group_by(HabilidadTecnica.nombre_habilidad_tecnica)
        .order_by(func.count(CandidatoConocimiento.id_conocimiento).desc())
        .limit(5)
        .all()
    )
    top_habilidades_tecnicas = [
        CountItem(label=h.label, count=h.count) for h in tecnicas_query
    ]

    # 3. Top 5 herramientas
    herramientas_query = (
        db.query(
            Herramienta.nombre_herramienta.label("label"),
            func.count(CandidatoConocimiento.id_conocimiento).label("count")
        )
        .join(Herramienta,
              CandidatoConocimiento.id_herramienta == Herramienta.id_herramienta)
        .filter(CandidatoConocimiento.tipo_conocimiento == 'herramienta')
        .group_by(Herramienta.nombre_herramienta)
        .order_by(func.count(CandidatoConocimiento.id_conocimiento).desc())
        .limit(5)
        .all()
    )
    top_herramientas = [
        CountItem(label=h.label, count=h.count) for h in herramientas_query
    ]

    return EstadisticasConocimientosResponse(
        top_habilidades_blandas=top_habilidades_blandas,
        top_habilidades_tecnicas=top_habilidades_tecnicas,
        top_herramientas=top_herramientas
    )
