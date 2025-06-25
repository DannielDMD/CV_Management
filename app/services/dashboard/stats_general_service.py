from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime, timedelta, date

from app.models.candidato_model import Candidato
from app.models.catalogs.cargo_ofrecido import CargoOfrecido
from app.models.catalogs.ciudad import Ciudad


def obtener_estadisticas_generales(db: Session, anio: int = None) -> dict:
    now = datetime.now()
    hoy = now.date()
    semana_pasada = now - timedelta(days=7)

    candidatos_q = db.query(Candidato)

    if anio:
        inicio_anio = date(anio, 1, 1)
        fin_anio = date(anio, 12, 31)
        candidatos_q = candidatos_q.filter(
            func.date(Candidato.fecha_registro).between(inicio_anio, fin_anio)
        )

    total_candidatos = candidatos_q.count()

    candidatos_hoy = db.query(Candidato).filter(
        func.date(Candidato.fecha_registro) == hoy
    ).count()

    candidatos_ultima_semana = db.query(Candidato).filter(
        Candidato.fecha_registro >= semana_pasada
    ).count()

    fechas_nacimiento = db.query(Candidato.fecha_nacimiento).all()
    edades = [
        hoy.year - fn[0].year - ((hoy.month, hoy.day) < (fn[0].month, fn[0].day))
        for fn in fechas_nacimiento if fn[0]
    ]
    edad_promedio = round(sum(edades) / len(edades), 1) if edades else 0.0

    # Distribución por mes (solo si hay año)
    candidatos_por_mes = {i: 0 for i in range(1, 13)}

    query_por_mes = db.query(
        extract("month", Candidato.fecha_registro).label("mes"),
        func.count(Candidato.id_candidato)
    )

    if anio:
        query_por_mes = query_por_mes.filter(
            func.date(Candidato.fecha_registro).between(date(anio, 1, 1), date(anio, 12, 31))
        )

    resultados_por_mes = query_por_mes.group_by("mes").order_by("mes").all()

    for mes, total in resultados_por_mes:
        candidatos_por_mes[int(mes)] = total

    ciudad_top = (
        db.query(Ciudad.nombre_ciudad, func.count(Candidato.id_candidato))
        .join(Candidato, Candidato.id_ciudad == Ciudad.id_ciudad)
        .group_by(Ciudad.nombre_ciudad)
        .order_by(func.count(Candidato.id_candidato).desc())
        .first()
    )

    cargo_top = (
        db.query(CargoOfrecido.nombre_cargo, func.count(Candidato.id_candidato))
        .join(Candidato, Candidato.id_cargo == CargoOfrecido.id_cargo)
        .group_by(CargoOfrecido.nombre_cargo)
        .order_by(func.count(Candidato.id_candidato).desc())
        .first()
    )

    # 🆕 Evolución por año-mes si no hay filtro de año
    evolucion_anual = None
    if anio is None:
        resultados = db.query(
            func.to_char(Candidato.fecha_registro, 'YYYY-MM').label('anio_mes'),
            func.count(Candidato.id_candidato)
        ).group_by('anio_mes').order_by('anio_mes').all()

        evolucion_anual = {row.anio_mes: row[1] for row in resultados}

    return {
        "total_candidatos": total_candidatos,
        "candidatos_hoy": candidatos_hoy,
        "candidatos_ultima_semana": candidatos_ultima_semana,
        "edad_promedio": edad_promedio,
        "candidatos_por_mes": candidatos_por_mes,
        "ciudad_top": ciudad_top[0] if ciudad_top else "N/A",
        "cargo_top": cargo_top[0] if cargo_top else "N/A",
        "evolucion_anual": evolucion_anual  # ✅ nuevo campo
    }
