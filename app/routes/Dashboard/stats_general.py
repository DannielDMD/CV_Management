from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime, timedelta, date

from app.core.database import get_db
from app.models.candidato_model import Candidato
from app.models.catalogs.ciudad import Ciudad
from app.models.catalogs.cargo_ofrecido import CargoOfrecido

router = APIRouter(prefix="/dashboard/stats", tags=["Dashboard General"])

@router.get("/general")
def get_general_stats(db: Session = Depends(get_db)):
    now = datetime.now()
    today = now.date()
    week_ago = now - timedelta(days=7)

    # Total de candidatos
    total_candidatos = db.query(Candidato).count()

    # Candidatos registrados hoy
    candidatos_hoy = db.query(Candidato).filter(func.date(Candidato.fecha_registro) == today).count()

    # Candidatos registrados en la última semana
    candidatos_ultima_semana = db.query(Candidato).filter(Candidato.fecha_registro >= week_ago).count()

    # Edad promedio
    fechas_nacimiento = db.query(Candidato.fecha_nacimiento).all()
    hoy = date.today()
    edades = [
        hoy.year - fn[0].year - ((hoy.month, hoy.day) < (fn[0].month, fn[0].day))
        for fn in fechas_nacimiento if fn[0]
    ]
    edad_promedio = round(sum(edades) / len(edades), 1) if edades else 0.0

    # Candidatos por mes (últimos 6 meses)
    seis_meses = now - timedelta(days=180)
    candidatos_por_mes = (
        db.query(
            extract("month", Candidato.fecha_registro).label("mes"),
            func.count(Candidato.id_candidato).label("total")
        )
        .filter(Candidato.fecha_registro >= seis_meses)
        .group_by("mes")
        .order_by("mes")
        .all()
    )
    candidatos_mes_dict = {int(mes): total for mes, total in candidatos_por_mes}

    # Ciudad con más candidatos
    ciudad_top = (
        db.query(Ciudad.nombre_ciudad, func.count(Candidato.id_candidato).label("total"))
        .join(Candidato, Candidato.id_ciudad == Ciudad.id_ciudad)
        .group_by(Ciudad.nombre_ciudad)
        .order_by(func.count(Candidato.id_candidato).desc())
        .first()
    )

    # Cargo más solicitado
    cargo_top = (
        db.query(CargoOfrecido.nombre_cargo, func.count(Candidato.id_candidato).label("total"))
        .join(Candidato, Candidato.id_cargo == CargoOfrecido.id_cargo)
        .group_by(CargoOfrecido.nombre_cargo)
        .order_by(func.count(Candidato.id_candidato).desc())
        .first()
    )

    return {
        "total_candidatos": total_candidatos,
        "candidatos_hoy": candidatos_hoy,
        "candidatos_ultima_semana": candidatos_ultima_semana,
        "edad_promedio": edad_promedio,
        "candidatos_por_mes": candidatos_mes_dict,
        "ciudad_top": ciudad_top[0] if ciudad_top else "N/A",
        "cargo_top": cargo_top[0] if cargo_top else "N/A"
    }
