# services/dashboard/stats_preferencias_service.py

from sqlalchemy.orm import Session
from sqlalchemy import func



from app.models.preferencias import Disponibilidad, MotivoSalida, PreferenciaDisponibilidad, RangoSalarial
from app.schemas.dashboard.stats_preferencias_schema import EstadisticasPreferenciasResponse
from app.schemas.dashboard.stats_personal_schema import CountItem

def obtener_estadisticas_preferencias(db: Session) -> EstadisticasPreferenciasResponse:
    """
    Recopila estadísticas de preferencias y disponibilidad de los candidatos:
     - Distribución por tipo de inicio de disponibilidad
     - Distribución por rangos salariales
     - Distribución por motivos de salida
     - Conteo de disponibilidad para viajar (Sí/No)
     - Conteo de situación laboral actual (Sí/No)
    """

    # 1. Distribución por disponibilidad de inicio
    disp_inicio_query = (
        db.query(
            Disponibilidad.descripcion_disponibilidad.label("label"),
            func.count(PreferenciaDisponibilidad.id_preferencia).label("count")
        )
        .join(PreferenciaDisponibilidad,
              PreferenciaDisponibilidad.id_disponibilidad_inicio == Disponibilidad.id_disponibilidad)
        .group_by(Disponibilidad.descripcion_disponibilidad)
        .order_by(func.count(PreferenciaDisponibilidad.id_preferencia).desc())
        .all()
    )
    disponibilidad_inicio = [
        CountItem(label=d.label, count=d.count) for d in disp_inicio_query
    ]

    # 2. Distribución por rangos salariales
    rangos_query = (
        db.query(
            RangoSalarial.descripcion_rango.label("label"),
            func.count(PreferenciaDisponibilidad.id_preferencia).label("count")
        )
        .join(PreferenciaDisponibilidad,
              PreferenciaDisponibilidad.id_rango_salarial == RangoSalarial.id_rango_salarial)
        .group_by(RangoSalarial.descripcion_rango)
        .order_by(func.count(PreferenciaDisponibilidad.id_preferencia).desc())
        .all()
    )
    rangos_salariales = [
        CountItem(label=r.label, count=r.count) for r in rangos_query
    ]

    # 3. Distribución por motivos de salida
    motivos_query = (
        db.query(
            MotivoSalida.descripcion_motivo.label("label"),
            func.count(PreferenciaDisponibilidad.id_preferencia).label("count")
        )
        .join(PreferenciaDisponibilidad,
              PreferenciaDisponibilidad.id_motivo_salida == MotivoSalida.id_motivo_salida)
        .filter(PreferenciaDisponibilidad.id_motivo_salida.isnot(None))
        .group_by(MotivoSalida.descripcion_motivo)
        .order_by(func.count(PreferenciaDisponibilidad.id_preferencia).desc())
        .all()
    )
    motivos_salida = [
        CountItem(label=m.label, count=m.count) for m in motivos_query
    ]

    # 4. Disponibilidad para viajar (Sí/No)
    viajar_true = db.query(func.count()).filter(PreferenciaDisponibilidad.disponibilidad_viajar == True).scalar()
    viajar_false = db.query(func.count()).filter(PreferenciaDisponibilidad.disponibilidad_viajar == False).scalar()
    disponibilidad_viajar = [
        CountItem(label="Sí", count=viajar_true),
        CountItem(label="No", count=viajar_false)
    ]

    # 5. Situación laboral actual (Sí/No)
    lab_true = db.query(func.count()).filter(PreferenciaDisponibilidad.trabaja_actualmente == True).scalar()
    lab_false = db.query(func.count()).filter(PreferenciaDisponibilidad.trabaja_actualmente == False).scalar()
    situacion_laboral_actual = [
        CountItem(label="Sí", count=lab_true),
        CountItem(label="No", count=lab_false)
    ]

    return EstadisticasPreferenciasResponse(
        disponibilidad_inicio=disponibilidad_inicio,
        rangos_salariales=rangos_salariales,
        motivos_salida=motivos_salida,
        disponibilidad_viajar=disponibilidad_viajar,
        situacion_laboral_actual=situacion_laboral_actual
    )
