# services/dashboard/stats_personal_service.py

from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date


from app.models.candidato_model import Candidato
from app.models.catalogs.cargo_ofrecido import CargoOfrecido
from app.models.catalogs.ciudad import Ciudad
from app.schemas.dashboard.stats_personal_schema import (
    CountItem,
    BooleanStats,
    EstadisticasPersonalesResponse
)


def obtener_estadisticas_personales(db: Session) -> EstadisticasPersonalesResponse:
    """
    Recopila estadísticas de información personal de los candidatos:
     - Top 5 ciudades con más candidatos
     - Top 5 cargos más solicitados
     - Distribución por rangos de edad
     - Conteo por estado del candidato
     - Estadísticas de campos booleanos clave
    """

    # 1. Top 5 ciudades
    ciudades_query = (
        db.query(
            Ciudad.nombre_ciudad.label("label"),
            func.count(Candidato.id_candidato).label("count")
        )
        .join(Candidato, Candidato.id_ciudad == Ciudad.id_ciudad)
        .group_by(Ciudad.nombre_ciudad)
        .order_by(func.count(Candidato.id_candidato).desc())
        .limit(5)
        .all()
    )
    top_ciudades = [CountItem(label=ciudad.label, count=ciudad.count) for ciudad in ciudades_query]

    # 2. Top 5 cargos
    cargos_query = (
        db.query(
            CargoOfrecido.nombre_cargo.label("label"),
            func.count(Candidato.id_candidato).label("count")
        )
        .join(Candidato, Candidato.id_cargo == CargoOfrecido.id_cargo)
        .group_by(CargoOfrecido.nombre_cargo)
        .order_by(func.count(Candidato.id_candidato).desc())
        .limit(5)
        .all()
    )
    top_cargos = [CountItem(label=cargo.label, count=cargo.count) for cargo in cargos_query]

    # 3. Rangos de edad
    hoy = date.today()
    nacimientos = db.query(Candidato.fecha_nacimiento).all()
    edades = [
        hoy.year - fn.year - ((hoy.month, hoy.day) < (fn.month, fn.day))
        for (fn,) in nacimientos
    ]
    rangos = {"<25": 0, "25-34": 0, "35-44": 0, "45+": 0}
    for edad in edades:
        if edad < 25:
            rangos["<25"] += 1
        elif edad < 35:
            rangos["25-34"] += 1
        elif edad < 45:
            rangos["35-44"] += 1
        else:
            rangos["45+"] += 1
    rangos_edad = [CountItem(label=k, count=v) for k, v in rangos.items()]

    # 4. Conteo por estado
    estados_query = (
        db.query(
            Candidato.estado.label("label"),
            func.count(Candidato.id_candidato).label("count")
        )
        .group_by(Candidato.estado)
        .all()
    )
    estado_candidatos = [CountItem(label=e.label, count=e.count) for e in estados_query]

    # 5. Estadísticas booleanas
    total_referidos = db.query(func.count()).filter(Candidato.tiene_referido == True).scalar()
    total_no_referidos = db.query(func.count()).filter(Candidato.tiene_referido == False).scalar()
    total_form_completos = db.query(func.count()).filter(Candidato.formulario_completo == True).scalar()
    total_form_incompletos = db.query(func.count()).filter(Candidato.formulario_completo == False).scalar()
    total_trabaja_joyco = db.query(func.count()).filter(Candidato.trabaja_actualmente_joyco == True).scalar()
    total_ha_trabajado = db.query(func.count()).filter(Candidato.ha_trabajado_joyco == True).scalar()

    estadisticas_booleanas = BooleanStats(
        referidos=total_referidos,
        no_referidos=total_no_referidos,
        formularios_completos=total_form_completos,
        formularios_incompletos=total_form_incompletos,
        trabaja_actualmente_joyco=total_trabaja_joyco,
        ha_trabajado_joyco=total_ha_trabajado
    )

    # 6. Ensamblar y devolver respuesta
    return EstadisticasPersonalesResponse(
        top_ciudades=top_ciudades,
        top_cargos=top_cargos,
        rangos_edad=rangos_edad,
        estado_candidatos=estado_candidatos,
        estadisticas_booleanas=estadisticas_booleanas
    )