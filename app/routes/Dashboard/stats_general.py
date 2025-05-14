from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime, timedelta, date

from app.core.database import get_db
from app.models.candidato_model import Candidato
from app.models.catalogs.ciudad import Ciudad
from app.models.catalogs.cargo_ofrecido import CargoOfrecido

router = APIRouter(prefix="/dashboard/stats", tags=["Dashboard General"])

@router.get("/general")
def get_general_stats(
    db: Session = Depends(get_db),
    anio: int = Query(None)  # 👉 Año opcional desde frontend
):
    now = datetime.now()
    hoy = now.date()
    semana_pasada = now - timedelta(days=7)

    # 👇 Si no se envía el año, se usa el actual
    anio = anio or now.year
    inicio_anio = date(anio, 1, 1)
    fin_anio = date(anio, 12, 31)

    # Total candidatos del año
    total_candidatos = db.query(Candidato).filter(
        func.date(Candidato.fecha_registro).between(inicio_anio, fin_anio)
    ).count()

    # Candidatos registrados hoy (no depende del año)
    candidatos_hoy = db.query(Candidato).filter(
        func.date(Candidato.fecha_registro) == hoy
    ).count()

    # Registrados en la última semana (tampoco depende del año)
    candidatos_ultima_semana = db.query(Candidato).filter(
        Candidato.fecha_registro >= semana_pasada
    ).count()

    # Edad promedio (en general)
    fechas_nacimiento = db.query(Candidato.fecha_nacimiento).all()
    edades = [
        hoy.year - fn[0].year - ((hoy.month, hoy.day) < (fn[0].month, fn[0].day))
        for fn in fechas_nacimiento if fn[0]
    ]
    edad_promedio = round(sum(edades) / len(edades), 1) if edades else 0.0

    # Candidatos por cada mes del año seleccionado
    resultados_por_mes = db.query(
        extract("month", Candidato.fecha_registro).label("mes"),
        func.count(Candidato.id_candidato)
    ).filter(
        func.date(Candidato.fecha_registro).between(inicio_anio, fin_anio)
    ).group_by("mes").order_by("mes").all()

    # Aseguramos que estén los 12 meses
    candidatos_por_mes = {i: 0 for i in range(1, 13)}
    for mes, total in resultados_por_mes:
        candidatos_por_mes[int(mes)] = total

    # Ciudad más registrada (todo el tiempo)
    ciudad_top = (
        db.query(Ciudad.nombre_ciudad, func.count(Candidato.id_candidato))
        .join(Candidato, Candidato.id_ciudad == Ciudad.id_ciudad)
        .group_by(Ciudad.nombre_ciudad)
        .order_by(func.count(Candidato.id_candidato).desc())
        .first()
    )

    # Cargo más solicitado (todo el tiempo)
    cargo_top = (
        db.query(CargoOfrecido.nombre_cargo, func.count(Candidato.id_candidato))
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
        "candidatos_por_mes": candidatos_por_mes,
        "ciudad_top": ciudad_top[0] if ciudad_top else "N/A",
        "cargo_top": cargo_top[0] if cargo_top else "N/A"
    }
