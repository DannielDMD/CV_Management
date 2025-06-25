# services/dashboard/stats_educacion_service.py

from collections import defaultdict
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, extract

from app.models.catalogs.instituciones import InstitucionAcademica
from app.models.catalogs.nivel_educacion import NivelEducacion
from app.models.catalogs.nivel_ingles import NivelIngles
from app.models.candidato_model import Candidato
from app.models.catalogs.titulo import TituloObtenido
from app.models.educacion_model import Educacion
from app.schemas.dashboard.stats_educacion_schema import EstadisticasEducacionResponse
from app.schemas.dashboard.stats_personal_schema import (
    CountItem,
    MonthCountItem,
    MonthTopItem,
)


def obtener_estadisticas_educacion(
    db: Session, año: Optional[int] = None
) -> EstadisticasEducacionResponse:
    """
    Recopila estadísticas de educación de los candidatos,
    opcionalmente filtradas por un año específico:
     - educaciones_por_mes: total de registros de educación cada mes del año
     - top_niveles_educacion_anual: Top 5 niveles de formación en todo el año
     - top_niveles_por_mes: nivel más frecuente por mes
     - top_titulos_obtenidos_anual: Top 5 títulos obtenidos en todo el año
     - top_titulos_por_mes: título más frecuente por mes
     - top_instituciones_academicas_anual: Top 5 instituciones en todo el año
     - top_instituciones_por_mes: institución más frecuente por mes
     - distribucion_nivel_ingles_anual: distribución por nivel de inglés anual
     - distribucion_nivel_ingles_por_mes: nivel de inglés más frecuente por mes
     - distribucion_anio_graduacion: conteo por año de graduación (todo el tiempo)
    """

    def año_filter(query):
        return (
            query.filter(extract("year", Candidato.fecha_registro) == año)
            if año
            else query
        )


# services/dashboard/stats_educacion_service.py

from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, extract

from app.models.catalogs.instituciones import InstitucionAcademica
from app.models.catalogs.nivel_educacion import NivelEducacion
from app.models.catalogs.nivel_ingles import NivelIngles
from app.models.candidato_model import Candidato
from app.models.catalogs.titulo import TituloObtenido
from app.models.educacion_model import Educacion
from app.schemas.dashboard.stats_educacion_schema import EstadisticasEducacionResponse
from app.schemas.dashboard.stats_personal_schema import (
    CountItem,
    MonthCountItem,
    MonthTopItem,
)


def obtener_estadisticas_educacion(
    db: Session, año: Optional[int] = None
) -> EstadisticasEducacionResponse:
    """
    Recopila estadísticas de educación de los candidatos,
    opcionalmente filtradas por un año específico:
     - educaciones_por_mes: total de registros de educación cada mes del año
     - top_niveles_educacion_anual: Top 5 niveles de formación en todo el año
     - top_niveles_por_mes: nivel más frecuente por mes
     - top_titulos_obtenidos_anual: Top 5 títulos obtenidos en todo el año
     - top_titulos_por_mes: título más frecuente por mes
     - top_instituciones_academicas_anual: Top 5 instituciones en todo el año
     - top_instituciones_por_mes: institución más frecuente por mes
     - distribucion_nivel_ingles_anual: distribución por nivel de inglés anual
     - distribucion_nivel_ingles_por_mes: nivel de inglés más frecuente por mes
     - distribucion_anio_graduacion: conteo por año de graduación (todo el tiempo)
    """

    def año_filter(query):
        return (
            query.filter(extract("year", Candidato.fecha_registro) == año)
            if año
            else query
        )

    # Educaciones por mes
    educ_mes_q = (
        año_filter(
            db.query(
                extract("month", Candidato.fecha_registro).label("month"),
                func.count(Educacion.id_educacion).label("count"),
            ).join(Educacion, Educacion.id_candidato == Candidato.id_candidato)
        )
        .group_by("month")
        .order_by("month")
        .all()
    )
    educaciones_por_mes = [
        MonthCountItem(month=int(r.month), count=r.count) for r in educ_mes_q
    ]

    # Top niveles educativos anual
    niv_anual_q = (
        año_filter(
            db.query(
                NivelEducacion.descripcion_nivel.label("label"),
                func.count(Educacion.id_educacion).label("count"),
            )
            .join(
                Educacion,
                Educacion.id_nivel_educacion == NivelEducacion.id_nivel_educacion,
            )
            .join(Candidato, Educacion.id_candidato == Candidato.id_candidato)
        )
        .group_by(NivelEducacion.descripcion_nivel)
        .order_by(func.count(Educacion.id_educacion).desc())
        .limit(5)
        .all()
    )
    top_niveles_educacion_anual = [
        CountItem(label=r.label, count=r.count) for r in niv_anual_q
    ]

    # Top niveles por mes
    top_niveles_por_mes = []
    for m in range(1, 13):
        row = (
            año_filter(
                db.query(
                    NivelEducacion.descripcion_nivel.label("label"),
                    func.count(Educacion.id_educacion).label("count"),
                )
                .join(
                    Educacion,
                    Educacion.id_nivel_educacion == NivelEducacion.id_nivel_educacion,
                )
                .join(Candidato, Educacion.id_candidato == Candidato.id_candidato)
            )
            .filter(extract("month", Candidato.fecha_registro) == m)
            .group_by(NivelEducacion.descripcion_nivel)
            .order_by(func.count(Educacion.id_educacion).desc())
            .limit(1)
            .first()
        )
        if row:
            top_niveles_por_mes.append(
                MonthTopItem(month=m, label=row.label, count=row.count)
            )

    # Top títulos obtenidos (catalogo + otros)
    tit_catalogo = (
        año_filter(
            db.query(
                TituloObtenido.nombre_titulo.label("label"),
                func.count(Educacion.id_educacion).label("count"),
            )
            .join(Educacion, Educacion.id_titulo == TituloObtenido.id_titulo)
            .join(Candidato, Educacion.id_candidato == Candidato.id_candidato)
        )
        .group_by(TituloObtenido.nombre_titulo)
        .all()
    )

    tit_otro = año_filter(
        db.query(
            Educacion.nombre_titulo_otro.label("label"),
            func.count(Educacion.id_educacion).label("count"),
        )
        .join(Candidato, Educacion.id_candidato == Candidato.id_candidato)
        .filter(
            Educacion.nombre_titulo_otro.isnot(None), Educacion.nombre_titulo_otro != ""
        )
        .group_by(Educacion.nombre_titulo_otro)
    ).all()

    mapa_titulos = defaultdict(int)
    for t in tit_catalogo + tit_otro:
        mapa_titulos[t.label] += t.count

    top_titulos_obtenidos_anual = sorted(
        [CountItem(label=k, count=v) for k, v in mapa_titulos.items()],
        key=lambda x: x.count,
        reverse=True,
    )[:5]

    top_titulos_por_mes = []
    for m in range(1, 13):
        cat_q = año_filter(
            db.query(
                TituloObtenido.nombre_titulo.label("label"),
                func.count(Educacion.id_educacion).label("count"),
            )
            .join(Educacion, Educacion.id_titulo == TituloObtenido.id_titulo)
            .join(Candidato, Educacion.id_candidato == Candidato.id_candidato)
            .filter(extract("month", Candidato.fecha_registro) == m)
            .group_by(TituloObtenido.nombre_titulo)
        ).all()

        otro_q = año_filter(
            db.query(
                Educacion.nombre_titulo_otro.label("label"),
                func.count(Educacion.id_educacion).label("count"),
            )
            .join(Candidato, Educacion.id_candidato == Candidato.id_candidato)
            .filter(
                extract("month", Candidato.fecha_registro) == m,
                Educacion.nombre_titulo_otro.isnot(None),
                Educacion.nombre_titulo_otro != "",
            )
            .group_by(Educacion.nombre_titulo_otro)
        ).all()

        mapa = defaultdict(int)
        for t in cat_q + otro_q:
            mapa[t.label] += t.count

        if mapa:
            label_top, count_top = max(mapa.items(), key=lambda x: x[1])
            top_titulos_por_mes.append(
                MonthTopItem(month=m, label=label_top, count=count_top)
            )

        # Top instituciones academicas (catalogo + otras)
    inst_catalogo = (
        año_filter(
            db.query(
                InstitucionAcademica.nombre_institucion.label("label"),
                func.count(Educacion.id_educacion).label("count"),
            )
            .join(
                Educacion,
                Educacion.id_institucion == InstitucionAcademica.id_institucion,
            )
            .join(Candidato, Educacion.id_candidato == Candidato.id_candidato)
        )
        .group_by(InstitucionAcademica.nombre_institucion)
        .all()
    )

    inst_otro = año_filter(
        db.query(
            Educacion.nombre_institucion_otro.label("label"),
            func.count(Educacion.id_educacion).label("count"),
        )
        .join(Candidato, Educacion.id_candidato == Candidato.id_candidato)
        .filter(
            Educacion.nombre_institucion_otro.isnot(None),
            Educacion.nombre_institucion_otro != "",
        )
        .group_by(Educacion.nombre_institucion_otro)
    ).all()

    mapa_instituciones = defaultdict(int)
    for i in inst_catalogo + inst_otro:
        mapa_instituciones[i.label] += i.count

    top_instituciones_academicas_anual = sorted(
        [CountItem(label=k, count=v) for k, v in mapa_instituciones.items()],
        key=lambda x: x.count,
        reverse=True,
    )[:5]

    top_instituciones_por_mes = []
    for m in range(1, 13):
        cat_q = año_filter(
            db.query(
                InstitucionAcademica.nombre_institucion.label("label"),
                func.count(Educacion.id_educacion).label("count"),
            )
            .join(
                Educacion,
                Educacion.id_institucion == InstitucionAcademica.id_institucion,
            )
            .join(Candidato, Educacion.id_candidato == Candidato.id_candidato)
            .filter(extract("month", Candidato.fecha_registro) == m)
            .group_by(InstitucionAcademica.nombre_institucion)
        ).all()

        otro_q = año_filter(
            db.query(
                Educacion.nombre_institucion_otro.label("label"),
                func.count(Educacion.id_educacion).label("count"),
            )
            .join(Candidato, Educacion.id_candidato == Candidato.id_candidato)
            .filter(
                extract("month", Candidato.fecha_registro) == m,
                Educacion.nombre_institucion_otro.isnot(None),
                Educacion.nombre_institucion_otro != "",
            )
            .group_by(Educacion.nombre_institucion_otro)
        ).all()

        mapa = defaultdict(int)
        for i in cat_q + otro_q:
            mapa[i.label] += i.count

        if mapa:
            label_top, count_top = max(mapa.items(), key=lambda x: x[1])
            top_instituciones_por_mes.append(
                MonthTopItem(month=m, label=label_top, count=count_top)
            )

    # 8. Inglés anual
    ing_anual_q = (
        año_filter(
            db.query(
                NivelIngles.nivel.label("label"),
                func.count(Educacion.id_educacion).label("count"),
            )
            .join(Educacion, Educacion.id_nivel_ingles == NivelIngles.id_nivel_ingles)
            .join(Candidato, Educacion.id_candidato == Candidato.id_candidato)
        )
        .group_by(NivelIngles.nivel)
        .order_by(func.count(Educacion.id_educacion).desc())
        .all()
    )
    distribucion_nivel_ingles_anual = [
        CountItem(label=r.label, count=r.count) for r in ing_anual_q
    ]

    # 9. Inglés por mes
    distribucion_nivel_ingles_por_mes = []
    for m in range(1, 13):
        row = (
            año_filter(
                db.query(
                    NivelIngles.nivel.label("label"),
                    func.count(Educacion.id_educacion).label("count"),
                )
                .join(
                    Educacion, Educacion.id_nivel_ingles == NivelIngles.id_nivel_ingles
                )
                .join(Candidato, Educacion.id_candidato == Candidato.id_candidato)
            )
            .filter(extract("month", Candidato.fecha_registro) == m)
            .group_by(NivelIngles.nivel)
            .order_by(func.count(Educacion.id_educacion).desc())
            .limit(1)
            .first()
        )
        if row:
            distribucion_nivel_ingles_por_mes.append(
                MonthTopItem(month=m, label=row.label, count=row.count)
            )

    # 10. Distribución año graduación (sin filtro)
# 10. Distribución año graduación (con filtro por año de registro del candidato)
    anios_q = (
        año_filter(
            db.query(
                Educacion.anio_graduacion.label("label"),
                func.count(Educacion.id_educacion).label("count"),
            )
            .join(Candidato, Educacion.id_candidato == Candidato.id_candidato)
            .filter(Educacion.anio_graduacion.isnot(None))
        )
        .group_by(Educacion.anio_graduacion)
        .order_by(func.count(Educacion.id_educacion).desc())
        .all()
    )

    distribucion_anio_graduacion = [
        CountItem(label=str(r.label), count=r.count) for r in anios_q
    ]


# Total de registros de educación
    total_educaciones = año_filter(
        db.query(func.count(Educacion.id_educacion))
        .join(Candidato, Educacion.id_candidato == Candidato.id_candidato)
    ).scalar()

    return EstadisticasEducacionResponse(
        educaciones_por_mes=educaciones_por_mes,
        top_niveles_educacion_anual=top_niveles_educacion_anual,
        top_niveles_por_mes=top_niveles_por_mes,
        top_titulos_obtenidos_anual=top_titulos_obtenidos_anual,
        top_titulos_por_mes=top_titulos_por_mes,
        top_instituciones_academicas_anual=top_instituciones_academicas_anual,
        top_instituciones_por_mes=top_instituciones_por_mes,
        distribucion_nivel_ingles_anual=distribucion_nivel_ingles_anual,
        distribucion_nivel_ingles_por_mes=distribucion_nivel_ingles_por_mes,
        distribucion_anio_graduacion=distribucion_anio_graduacion,
        total_educaciones=total_educaciones  # ✅ INCLUIDO EN RESPUESTA
    )
