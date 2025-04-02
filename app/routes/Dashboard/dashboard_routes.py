"""from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from app.core.database import get_db
from app.models.candidato_model import Candidato
from app.models.experiencia_model import ExperienciaLaboral
from app.models.conocimientos_model import CandidatoConocimiento, HabilidadTecnica

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    # Total de candidatos
    total_candidatos = db.query(Candidato).count()

    # Candidatos registrados en la última semana
    start_of_week = datetime.now() - timedelta(days=7)
    nuevos_esta_semana = db.query(Candidato).filter(Candidato.fecha_registro >= start_of_week).count()

    # Promedio de experiencia en años
    experiencias = db.query(ExperienciaLaboral).all()
    total_experiencias = len(experiencias)
    total_anios = 0

    for exp in experiencias:
        if exp.fecha_fin and exp.fecha_inicio:
            diferencia = (exp.fecha_fin - exp.fecha_inicio).days / 365
            total_anios += max(diferencia, 0)  # Evitar negativos por errores

    promedio_experiencia = round(total_anios / total_experiencias, 1) if total_experiencias > 0 else 0.0

    # Habilidad técnica más común
    top_skill = (
        db.query(CandidatoConocimiento.id_habilidad_tecnica, func.count(CandidatoConocimiento.id_habilidad_tecnica).label("conteo"))
        .filter(CandidatoConocimiento.tipo_conocimiento == "tecnica", CandidatoConocimiento.id_habilidad_tecnica != None)
        .group_by(CandidatoConocimiento.id_habilidad_tecnica)
        .order_by(func.count(CandidatoConocimiento.id_habilidad_tecnica).desc())
        .first()
    )

    skill_nombre = None
    if top_skill:
        habilidad = db.query(HabilidadTecnica).filter(HabilidadTecnica.id_habilidad_tecnica == top_skill[0]).first()
        skill_nombre = habilidad.nombre_habilidad_tecnica if habilidad else "N/A"

    return {
        "total_candidatos": total_candidatos,
        "nuevos_esta_semana": nuevos_esta_semana,
        "promedio_experiencia": promedio_experiencia,
        "skill_mas_comun": skill_nombre or "N/A"
    }"""