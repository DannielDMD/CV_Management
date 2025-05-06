# services/dashboard/stats_educacion_service.py

from sqlalchemy.orm import Session
from sqlalchemy import func


from app.models.catalogs.instituciones import InstitucionAcademica
from app.models.catalogs.nivel_educacion import NivelEducacion
from app.models.catalogs.nivel_ingles import NivelIngles
from app.models.catalogs.titulo import TituloObtenido
from app.models.educacion_model import Educacion
from app.schemas.dashboard.stats_educacion_schema import EstadisticasEducacionResponse
from app.schemas.dashboard.stats_personal_schema import CountItem


def obtener_estadisticas_educacion(db: Session) -> EstadisticasEducacionResponse:
    """
    Recopila estadísticas de educación de los candidatos:
     - Top 5 niveles de formación
     - Top 5 títulos obtenidos
     - Top 5 instituciones académicas
     - Distribución por nivel de inglés
     - Distribución por año de graduación (top 5 años)
    """

    # 1. Top 5 niveles educativos
    niveles_query = (
        db.query(
            NivelEducacion.descripcion_nivel.label("label"),
            func.count(Educacion.id_educacion).label("count")
        )
        .join(Educacion, Educacion.id_nivel_educacion == NivelEducacion.id_nivel_educacion)
        .group_by(NivelEducacion.descripcion_nivel)
        .order_by(func.count(Educacion.id_educacion).desc())
        .limit(5)
        .all()
    )
    top_niveles_educacion = [
        CountItem(label=nv.label, count=nv.count) for nv in niveles_query
    ]

    # 2. Top 5 títulos obtenidos
    titulos_query = (
        db.query(
            TituloObtenido.nombre_titulo.label("label"),
            func.count(Educacion.id_educacion).label("count")
        )
        .join(Educacion, Educacion.id_titulo == TituloObtenido.id_titulo)
        .group_by(TituloObtenido.nombre_titulo)
        .order_by(func.count(Educacion.id_educacion).desc())
        .limit(5)
        .all()
    )
    top_titulos_obtenidos = [
        CountItem(label=t.label, count=t.count) for t in titulos_query
    ]

    # 3. Top 5 instituciones académicas
    insts_query = (
        db.query(
            InstitucionAcademica.nombre_institucion.label("label"),
            func.count(Educacion.id_educacion).label("count")
        )
        .join(Educacion, Educacion.id_institucion == InstitucionAcademica.id_institucion)
        .group_by(InstitucionAcademica.nombre_institucion)
        .order_by(func.count(Educacion.id_educacion).desc())
        .limit(5)
        .all()
    )
    top_instituciones_academicas = [
        CountItem(label=i.label, count=i.count) for i in insts_query
    ]

    # 4. Distribución por nivel de inglés
    ingles_query = (
        db.query(
            NivelIngles.nivel.label("label"),
            func.count(Educacion.id_educacion).label("count")
        )
        .join(Educacion, Educacion.id_nivel_ingles == NivelIngles.id_nivel_ingles)
        .group_by(NivelIngles.nivel)
        .order_by(func.count(Educacion.id_educacion).desc())
        .all()
    )
    distribucion_nivel_ingles = [
        CountItem(label=ing.label, count=ing.count) for ing in ingles_query
    ]

    # 5. Distribución por año de graduación (top 5 años)
    anios_query = (
        db.query(
            Educacion.anio_graduacion.label("label"),
            func.count(Educacion.id_educacion).label("count")
        )
        .filter(Educacion.anio_graduacion.isnot(None))
        .group_by(Educacion.anio_graduacion)
        .order_by(func.count(Educacion.id_educacion).desc())
        .limit(5)
        .all()
    )
    distribucion_anio_graduacion = [
        CountItem(label=str(a.label), count=a.count) for a in anios_query
    ]

    return EstadisticasEducacionResponse(
        top_niveles_educacion=top_niveles_educacion,
        top_titulos_obtenidos=top_titulos_obtenidos,
        top_instituciones_academicas=top_instituciones_academicas,
        distribucion_nivel_ingles=distribucion_nivel_ingles,
        distribucion_anio_graduacion=distribucion_anio_graduacion
    )
