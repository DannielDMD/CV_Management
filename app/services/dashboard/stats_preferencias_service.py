# services/dashboard/stats_preferencias_service.py

from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, extract

from app.models.candidato_model import Candidato
from app.models.preferencias import PreferenciaDisponibilidad, Disponibilidad, RangoSalarial, MotivoSalida
from app.schemas.dashboard.stats_preferencias_schema import EstadisticasPreferenciasResponse
from app.schemas.dashboard.stats_personal_schema import CountItem, MonthCountItem, MonthTopItem

def obtener_estadisticas_preferencias(
    db: Session,
    año: Optional[int] = None
) -> EstadisticasPreferenciasResponse:
    """
    Recopila estadísticas de preferencias y disponibilidad de los candidatos,
    opcionalmente filtradas por un año específico:
     - preferencias_por_mes: total de registros por mes
     - top_disponibilidad_inicio_anual / _por_mes
     - top_rangos_salariales_anual / _por_mes
     - top_motivos_salida_anual / _por_mes
     - disponibilidad_viajar_anual / _por_mes
     - situacion_laboral_actual_anual / _por_mes
    """
    def aplicar_filtro_año(query):
        if año:
            return query.filter(extract("year", Candidato.fecha_registro) == año)
        return query

    # 1. Preferencias por mes
    q = (
        db.query(
            extract("month", Candidato.fecha_registro).label("month"),
            func.count(PreferenciaDisponibilidad.id_preferencia).label("count")
        )
        .join(PreferenciaDisponibilidad, PreferenciaDisponibilidad.id_candidato == Candidato.id_candidato)
    )
    mes_q = aplicar_filtro_año(q).group_by("month").order_by("month").all()
    preferencias_por_mes = [
        MonthCountItem(month=int(r.month), count=r.count) for r in mes_q
    ]

    # 2. Disponibilidad de inicio anual
    q2 = (
        db.query(
            Disponibilidad.descripcion_disponibilidad.label("label"),
            func.count(PreferenciaDisponibilidad.id_preferencia).label("count")
        )
        .join(PreferenciaDisponibilidad, PreferenciaDisponibilidad.id_disponibilidad_inicio == Disponibilidad.id_disponibilidad)
        .join(Candidato, PreferenciaDisponibilidad.id_candidato == Candidato.id_candidato)
    )
    disp_anual_q = aplicar_filtro_año(q2).group_by(Disponibilidad.descripcion_disponibilidad)\
        .order_by(func.count(PreferenciaDisponibilidad.id_preferencia).desc())\
        .all()
    top_disponibilidad_inicio_anual = [
        CountItem(label=r.label, count=r.count) for r in disp_anual_q
    ]

    # 3. Disponibilidad de inicio por mes
    top_disponibilidad_inicio_por_mes = []
    for m in range(1, 13):
        row = aplicar_filtro_año(
            db.query(
                Disponibilidad.descripcion_disponibilidad.label("label"),
                func.count(PreferenciaDisponibilidad.id_preferencia).label("count")
            )
            .join(PreferenciaDisponibilidad, PreferenciaDisponibilidad.id_disponibilidad_inicio == Disponibilidad.id_disponibilidad)
            .join(Candidato, PreferenciaDisponibilidad.id_candidato == Candidato.id_candidato)
            .filter(extract("month", Candidato.fecha_registro) == m)
            .group_by(Disponibilidad.descripcion_disponibilidad)
            .order_by(func.count(PreferenciaDisponibilidad.id_preferencia).desc())
        ).first()
        if row:
            top_disponibilidad_inicio_por_mes.append(
                MonthTopItem(month=m, label=row.label, count=row.count)
            )

    # 4. Rangos salariales anual
    q3 = (
        db.query(
            RangoSalarial.descripcion_rango.label("label"),
            func.count(PreferenciaDisponibilidad.id_preferencia).label("count")
        )
        .join(PreferenciaDisponibilidad, PreferenciaDisponibilidad.id_rango_salarial == RangoSalarial.id_rango_salarial)
        .join(Candidato, PreferenciaDisponibilidad.id_candidato == Candidato.id_candidato)
    )
    rangos_anual_q = aplicar_filtro_año(q3).group_by(RangoSalarial.descripcion_rango)\
        .order_by(func.count(PreferenciaDisponibilidad.id_preferencia).desc())\
        .all()
    top_rangos_salariales_anual = [
        CountItem(label=r.label, count=r.count) for r in rangos_anual_q
    ]

    # 5. Rangos salariales por mes
    top_rangos_salariales_por_mes = []
    for m in range(1, 13):
        row = aplicar_filtro_año(
            db.query(
                RangoSalarial.descripcion_rango.label("label"),
                func.count(PreferenciaDisponibilidad.id_preferencia).label("count")
            )
            .join(PreferenciaDisponibilidad, PreferenciaDisponibilidad.id_rango_salarial == RangoSalarial.id_rango_salarial)
            .join(Candidato, PreferenciaDisponibilidad.id_candidato == Candidato.id_candidato)
            .filter(extract("month", Candidato.fecha_registro) == m)
            .group_by(RangoSalarial.descripcion_rango)
            .order_by(func.count(PreferenciaDisponibilidad.id_preferencia).desc())
        ).first()
        if row:
            top_rangos_salariales_por_mes.append(
                MonthTopItem(month=m, label=row.label, count=row.count)
            )

    # 6. Motivos de salida anual
    q4 = (
        db.query(
            MotivoSalida.descripcion_motivo.label("label"),
            func.count(PreferenciaDisponibilidad.id_preferencia).label("count")
        )
        .join(PreferenciaDisponibilidad, PreferenciaDisponibilidad.id_motivo_salida == MotivoSalida.id_motivo_salida)
        .filter(PreferenciaDisponibilidad.id_motivo_salida.isnot(None))
        .join(Candidato, PreferenciaDisponibilidad.id_candidato == Candidato.id_candidato)
    )
    motivos_anual_q = aplicar_filtro_año(q4)\
        .group_by(MotivoSalida.descripcion_motivo)\
        .order_by(func.count(PreferenciaDisponibilidad.id_preferencia).desc())\
        .all()
    top_motivos_salida_anual = [
        CountItem(label=r.label, count=r.count) for r in motivos_anual_q
    ]

    # 7. Motivos de salida por mes
    top_motivos_salida_por_mes = []
    for m in range(1, 13):
        row = aplicar_filtro_año(
            db.query(
                MotivoSalida.descripcion_motivo.label("label"),
                func.count(PreferenciaDisponibilidad.id_preferencia).label("count")
            )
            .join(PreferenciaDisponibilidad, PreferenciaDisponibilidad.id_motivo_salida == MotivoSalida.id_motivo_salida)
            .join(Candidato, PreferenciaDisponibilidad.id_candidato == Candidato.id_candidato)
            .filter(PreferenciaDisponibilidad.id_motivo_salida.isnot(None))
            .filter(extract("month", Candidato.fecha_registro) == m)
            .group_by(MotivoSalida.descripcion_motivo)
            .order_by(func.count(PreferenciaDisponibilidad.id_preferencia).desc())
        ).first()
        if row:
            top_motivos_salida_por_mes.append(
                MonthTopItem(month=m, label=row.label, count=row.count)
            )

    # 8. Disponibilidad para viajar anual
    q5_true = (
        db.query(func.count(PreferenciaDisponibilidad.id_preferencia))
        .filter(PreferenciaDisponibilidad.disponibilidad_viajar == True)
        .join(Candidato, PreferenciaDisponibilidad.id_candidato == Candidato.id_candidato)
    )
    q5_false = (
        db.query(func.count(PreferenciaDisponibilidad.id_preferencia))
        .filter(PreferenciaDisponibilidad.disponibilidad_viajar == False)
        .join(Candidato, PreferenciaDisponibilidad.id_candidato == Candidato.id_candidato)
    )
    viajar_true = aplicar_filtro_año(q5_true).scalar()
    viajar_false = aplicar_filtro_año(q5_false).scalar()
    disponibilidad_viajar_anual = [
        CountItem(label="Sí", count=viajar_true),
        CountItem(label="No", count=viajar_false),
    ]

    # 9. Disponibilidad para viajar por mes
    disponibilidad_viajar_por_mes = []
    for m in range(1, 13):
        q_yes = (
            db.query(func.count(PreferenciaDisponibilidad.id_preferencia).label("count"))
            .filter(PreferenciaDisponibilidad.disponibilidad_viajar == True)
            .join(Candidato, PreferenciaDisponibilidad.id_candidato == Candidato.id_candidato)
            .filter(extract("month", Candidato.fecha_registro) == m)
        )
        q_no = (
            db.query(func.count(PreferenciaDisponibilidad.id_preferencia).label("count"))
            .filter(PreferenciaDisponibilidad.disponibilidad_viajar == False)
            .join(Candidato, PreferenciaDisponibilidad.id_candidato == Candidato.id_candidato)
            .filter(extract("month", Candidato.fecha_registro) == m)
        )
        yes = aplicar_filtro_año(q_yes).scalar() or 0
        no = aplicar_filtro_año(q_no).scalar() or 0
        if yes or no:
            label = "Sí" if yes >= no else "No"
            count = max(yes, no)
            disponibilidad_viajar_por_mes.append(
                MonthTopItem(month=m, label=label, count=count)
            )

    # 10. Situación laboral actual anual
    q6_true = (
        db.query(func.count(PreferenciaDisponibilidad.id_preferencia))
        .filter(PreferenciaDisponibilidad.trabaja_actualmente == True)
        .join(Candidato, PreferenciaDisponibilidad.id_candidato == Candidato.id_candidato)
    )
    q6_false = (
        db.query(func.count(PreferenciaDisponibilidad.id_preferencia))
        .filter(PreferenciaDisponibilidad.trabaja_actualmente == False)
        .join(Candidato, PreferenciaDisponibilidad.id_candidato == Candidato.id_candidato)
    )
    lab_true = aplicar_filtro_año(q6_true).scalar()
    lab_false = aplicar_filtro_año(q6_false).scalar()
    situacion_laboral_actual_anual = [
        CountItem(label="Sí", count=lab_true),
        CountItem(label="No", count=lab_false),
    ]

    # 11. Situación laboral actual por mes
    situacion_laboral_actual_por_mes = []
    for m in range(1, 13):
        q_yes = (
            db.query(func.count(PreferenciaDisponibilidad.id_preferencia).label("count"))
            .filter(PreferenciaDisponibilidad.trabaja_actualmente == True)
            .join(Candidato, PreferenciaDisponibilidad.id_candidato == Candidato.id_candidato)
            .filter(extract("month", Candidato.fecha_registro) == m)
        )
        q_no = (
            db.query(func.count(PreferenciaDisponibilidad.id_preferencia).label("count"))
            .filter(PreferenciaDisponibilidad.trabaja_actualmente == False)
            .join(Candidato, PreferenciaDisponibilidad.id_candidato == Candidato.id_candidato)
            .filter(extract("month", Candidato.fecha_registro) == m)
        )
        yes = aplicar_filtro_año(q_yes).scalar() or 0
        no = aplicar_filtro_año(q_no).scalar() or 0
        if yes or no:
            label = "Sí" if yes >= no else "No"
            count = max(yes, no)
            situacion_laboral_actual_por_mes.append(
                MonthTopItem(month=m, label=label, count=count)
            )

    return EstadisticasPreferenciasResponse(
        preferencias_por_mes=preferencias_por_mes,
        top_disponibilidad_inicio_anual=top_disponibilidad_inicio_anual,
        top_disponibilidad_inicio_por_mes=top_disponibilidad_inicio_por_mes,
        top_rangos_salariales_anual=top_rangos_salariales_anual,
        top_rangos_salariales_por_mes=top_rangos_salariales_por_mes,
        top_motivos_salida_anual=top_motivos_salida_anual,
        top_motivos_salida_por_mes=top_motivos_salida_por_mes,
        disponibilidad_viajar_anual=disponibilidad_viajar_anual,
        disponibilidad_viajar_por_mes=disponibilidad_viajar_por_mes,
        situacion_laboral_actual_anual=situacion_laboral_actual_anual,
        situacion_laboral_actual_por_mes=situacion_laboral_actual_por_mes,
    )
