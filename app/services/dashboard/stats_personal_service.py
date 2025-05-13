# services/dashboard/stats_personal_service.py

from typing import Optional
from io import BytesIO
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import func, extract

from app.models.candidato_model import Candidato
from app.models.catalogs.cargo_ofrecido import CargoOfrecido
from app.models.catalogs.ciudad import Ciudad
from app.schemas.dashboard.stats_personal_schema import (
    CountItem,
    BooleanStats,
    MonthCountItem,
    MonthTopItem,
    EstadisticasPersonalesResponse,
)

def obtener_estadisticas_personales(
    db: Session,
    año: Optional[int] = None
) -> EstadisticasPersonalesResponse:
    """
    Recopila estadísticas de información personal de los candidatos,
    opcionalmente filtradas por un año específico:
     - candidatos_por_mes: total de candidatos registrados cada mes
     - top_ciudades_anual: top 5 ciudades en todo el año
     - top_ciudades_por_mes: ciudad más frecuente por cada mes
     - rangos_edad: distribución de edad (todo el año o en el año)
     - estado_candidatos: conteo de estados (todo el año o en el año)
     - estadisticas_booleanas: campos booleanos (todo el año o en el año)
     - top_cargos_anual: top 5 cargos en todo el año
     - top_cargos_por_mes: cargo más frecuente por cada mes
    """

    # Base filter for year
    def año_filter(query, fecha_col):
        if año:
            return query.filter(extract("year", fecha_col) == año)
        return query

    # 1. Candidatos por mes
    mes_query = (
        año_filter(
            db.query(
                extract("month", Candidato.fecha_registro).label("month"),
                func.count(Candidato.id_candidato).label("count")
            ),
            Candidato.fecha_registro
        )
        .group_by("month")
        .order_by("month")
        .all()
    )
    candidatos_por_mes = [
        MonthCountItem(month=int(m.month), count=m.count) for m in mes_query
    ]

    # 2. Top 5 ciudades anual
    ciudades_anual_q = (
        año_filter(
            db.query(
                Ciudad.nombre_ciudad.label("label"),
                func.count(Candidato.id_candidato).label("count")
            ),
            Candidato.fecha_registro
        )
        .join(Candidato, Candidato.id_ciudad == Ciudad.id_ciudad)
        .group_by(Ciudad.nombre_ciudad)
        .order_by(func.count(Candidato.id_candidato).desc())
        .limit(5)
        .all()
    )
    top_ciudades_anual = [
        CountItem(label=c.label, count=c.count) for c in ciudades_anual_q
    ]

    # 3. Top ciudad por mes
    top_ciudades_por_mes = []
    for m in range(1, 13):
        row = (
            año_filter(
                db.query(
                    Ciudad.nombre_ciudad.label("label"),
                    func.count(Candidato.id_candidato).label("count")
                ).join(Candidato, Candidato.id_ciudad == Ciudad.id_ciudad),
                Candidato.fecha_registro
            )
            .filter(extract("month", Candidato.fecha_registro) == m)
            .group_by(Ciudad.nombre_ciudad)
            .order_by(func.count(Candidato.id_candidato).desc())
            .limit(1)
            .first()
        )
        if row:
            top_ciudades_por_mes.append(
                MonthTopItem(month=m, label=row.label, count=row.count)
            )

    # 4. Rangos de edad (sin mes, pero opcionalmente filtrar candidatos del año)
    hoy = date.today()
    nacimientos = (
        año_filter(
            db.query(Candidato.fecha_nacimiento),
            Candidato.fecha_registro
        )
        .filter(Candidato.fecha_nacimiento.isnot(None))
        .all()
    )
    edades = [
        hoy.year - fn.year - ((hoy.month, hoy.day) < (fn.month, fn.day))
        for (fn,) in nacimientos
    ]
    buckets = {"<25": 0, "25-34": 0, "35-44": 0, "45+": 0}
    for edad in edades:
        if edad < 25:
            buckets["<25"] += 1
        elif edad < 35:
            buckets["25-34"] += 1
        elif edad < 45:
            buckets["35-44"] += 1
        else:
            buckets["45+"] += 1
    rangos_edad = [CountItem(label=k, count=v) for k, v in buckets.items()]

    # 5. Conteo por estado
    estados_q = (
        año_filter(
            db.query(
                Candidato.estado.label("label"),
                func.count(Candidato.id_candidato).label("count")
            ),
            Candidato.fecha_registro
        )
        .group_by(Candidato.estado)
        .all()
    )
    estado_candidatos = [
        CountItem(label=e.label, count=e.count) for e in estados_q
    ]

    # 6. Estadísticas booleanas
    def boolean_count(cond):
        q = año_filter(
            db.query(func.count()).filter(cond),
            Candidato.fecha_registro
        )
        return q.scalar()

    estadisticas_booleanas = BooleanStats(
        referidos=boolean_count(Candidato.tiene_referido == True),
        no_referidos=boolean_count(Candidato.tiene_referido == False),
        formularios_completos=boolean_count(Candidato.formulario_completo == True),
        formularios_incompletos=boolean_count(Candidato.formulario_completo == False),
        trabaja_actualmente_joyco=boolean_count(Candidato.trabaja_actualmente_joyco == True),
        ha_trabajado_joyco=boolean_count(Candidato.ha_trabajado_joyco == True),
    )

    # 7. Top 5 cargos anual
    cargos_anual_q = (
        año_filter(
            db.query(
                CargoOfrecido.nombre_cargo.label("label"),
                func.count(Candidato.id_candidato).label("count")
            ),
            Candidato.fecha_registro
        )
        .join(Candidato, Candidato.id_cargo == CargoOfrecido.id_cargo)
        .group_by(CargoOfrecido.nombre_cargo)
        .order_by(func.count(Candidato.id_candidato).desc())
        .limit(5)
        .all()
    )
    top_cargos_anual = [
        CountItem(label=c.label, count=c.count) for c in cargos_anual_q
    ]

    # 8. Top cargos por mes
    top_cargos_por_mes = []
    for m in range(1, 13):
        row = (
            año_filter(
                db.query(
                    CargoOfrecido.nombre_cargo.label("label"),
                    func.count(Candidato.id_candidato).label("count")
                ).join(Candidato, Candidato.id_cargo == CargoOfrecido.id_cargo),
                Candidato.fecha_registro
            )
            .filter(extract("month", Candidato.fecha_registro) == m)
            .group_by(CargoOfrecido.nombre_cargo)
            .order_by(func.count(Candidato.id_candidato).desc())
            .limit(1)
            .first()
        )
        if row:
            top_cargos_por_mes.append(
                MonthTopItem(month=m, label=row.label, count=row.count)
            )
    # 9. Top nombres de referidos (donde sí hay nombre registrado)
    referidos_q = (
        año_filter(
            db.query(
                Candidato.nombre_referido.label("label"),
                func.count(Candidato.id_candidato).label("count")
            ).filter(Candidato.nombre_referido.isnot(None), Candidato.nombre_referido != ""),
            Candidato.fecha_registro
        )
        .group_by(Candidato.nombre_referido)
        .order_by(func.count(Candidato.id_candidato).desc())
        .limit(3)
        .all()
    )

    top_nombres_referidos = [
        CountItem(label=r.label, count=r.count) for r in referidos_q
    ]


    return EstadisticasPersonalesResponse(
        candidatos_por_mes=candidatos_por_mes,
        top_ciudades_anual=top_ciudades_anual,
        top_ciudades_por_mes=top_ciudades_por_mes,
        rangos_edad=rangos_edad,
        estado_candidatos=estado_candidatos,
        estadisticas_booleanas=estadisticas_booleanas,
        top_cargos_anual=top_cargos_anual,
        top_cargos_por_mes=top_cargos_por_mes,
        top_nombres_referidos=top_nombres_referidos  # 👈 nuevo
    )
