from datetime import datetime, timedelta, timezone
import logging
from typing import Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc, extract, func, or_
from fastapi import HTTPException
from app.models.candidato_model import Candidato
from app.models.catalogs.ciudad import Ciudad
from app.schemas.candidato_schema import (
    CandidatoCreate,
    CandidatoUpdate,
    CandidatoDetalleResponse,
)
from app.models.educacion_model import Educacion
from app.models.experiencia_model import ExperienciaLaboral
from app.models.conocimientos_model import CandidatoConocimiento
from app.models.preferencias import PreferenciaDisponibilidad
from app.models.catalogs.cargo_ofrecido import CargoOfrecido
from app.services.mappers.candidato_mapper import (
    mapear_candidato_detalle,
    mapear_candidato_resumen,
)


# Configurar logging
logger = logging.getLogger(__name__)


def create_candidato(db: Session, candidato_data: CandidatoCreate):
    if (
        db.query(Candidato)
        .filter(Candidato.correo_electronico == candidato_data.correo_electronico)
        .first()
    ):
        raise HTTPException(
            status_code=400, detail="El correo electrónico ya está registrado"
        )

    campos = candidato_data.model_dump()
    nuevo_candidato = Candidato(**campos)

    try:
        db.add(nuevo_candidato)
        db.commit()
        db.refresh(nuevo_candidato)  # 🔥 Esto recupera el ID generado
        print(f"Nuevo ID generado: {nuevo_candidato.id_candidato}")  # ✅ Debug
        return nuevo_candidato
    except IntegrityError as e:
        logger.error(f"Error de integridad al insertar candidato: {e}")
        db.rollback()
        raise HTTPException(
            status_code=500, detail="Error al insertar el candidato en la base de datos"
        )


def get_candidato_by_id(db: Session, id_candidato: int):
    candidato = db.get(Candidato, id_candidato)
    if not candidato:
        raise HTTPException(status_code=404, detail="Candidato no encontrado")
    return candidato


def get_all_candidatos(db: Session):
    return db.query(Candidato).all()


def update_candidato(db: Session, id_candidato: int, candidato_data: CandidatoUpdate):
    candidato = db.get(Candidato, id_candidato)
    if not candidato:
        raise HTTPException(status_code=404, detail="Candidato no encontrado")

    cambios = candidato_data.model_dump(exclude_unset=True)
    if not cambios:
        raise HTTPException(status_code=400, detail="No hay datos para actualizar")

    for key, value in cambios.items():
        setattr(candidato, key, value)

    try:
        db.commit()
        db.refresh(candidato)
        return candidato
    except IntegrityError as e:
        logger.error(f"Error al actualizar candidato: {e}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Error al actualizar el candidato en la base de datos",
        )


def delete_candidato(db: Session, id_candidato: int):
    candidato = db.get(Candidato, id_candidato)
    if not candidato:
        raise HTTPException(status_code=404, detail="Candidato no encontrado")

    db.delete(candidato)
    try:
        db.commit()
        return {
            "message": f"Candidato {candidato.nombre_completo} eliminado correctamente"
        }
    except Exception as e:
        logger.error(f"Error al eliminar candidato: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al eliminar el candidato")


def get_candidatos_resumen(
    db: Session,
    search: str = None,
    estado: str = None,
    id_disponibilidad: int = None,
    id_cargo: int = None,
    id_ciudad: int = None,
    id_herramienta: int = None,
    id_habilidad_tecnica: int = None,
    id_nivel_ingles: int = None,
    id_experiencia: int = None,
    id_titulo: int = None,
    trabaja_joyco: bool = None,
    ordenar_por_fecha: Optional[str] = None,
    anio: Optional[int] = None,
    mes: Optional[int] = None,
    skip: int = 0,
    limit: int = 10,
    # Nuevos filtros
    id_nivel_educacion: int = None,
    id_habilidad_blanda: int = None,
    id_rango_salarial: int = None,
    ha_trabajado_joyco: bool = None,
    tiene_referido: bool = None,
    disponibilidad_viajar: bool = None,
    trabaja_actualmente: bool = None,
):
    query = db.query(Candidato).options(
        joinedload(Candidato.ciudad),
        joinedload(Candidato.cargo),
        joinedload(Candidato.educaciones).joinedload(Educacion.nivel_educacion),
        joinedload(Candidato.educaciones).joinedload(Educacion.titulo),
        joinedload(Candidato.experiencias).joinedload(
            ExperienciaLaboral.rango_experiencia
        ),
        joinedload(Candidato.conocimientos).joinedload(
            CandidatoConocimiento.habilidad_blanda
        ),
        joinedload(Candidato.conocimientos).joinedload(
            CandidatoConocimiento.habilidad_tecnica
        ),
        joinedload(Candidato.conocimientos).joinedload(
            CandidatoConocimiento.herramienta
        ),
        joinedload(Candidato.preferencias).joinedload(
            PreferenciaDisponibilidad.disponibilidad
        ),
    )

    # Filtros
    if search:
        query = query.join(Candidato.cargo).filter(
            or_(
                Candidato.nombre_completo.ilike(f"%{search}%"),
                Candidato.correo_electronico.ilike(f"%{search}%"),
                CargoOfrecido.nombre_cargo.ilike(f"%{search}%"),
            )
        )
    if estado:
        query = query.filter(Candidato.estado == estado)
        
    if id_disponibilidad:
        query = query.join(Candidato.preferencias).filter(
            PreferenciaDisponibilidad.id_disponibilidad_inicio == id_disponibilidad
        )

        
    if id_cargo:
        query = query.filter(Candidato.id_cargo == id_cargo)
    if id_ciudad:
        query = query.filter(Candidato.id_ciudad == id_ciudad)
    if trabaja_joyco is not None:
        query = query.filter(Candidato.trabaja_actualmente_joyco == trabaja_joyco)
    if id_herramienta:
        query = query.join(Candidato.conocimientos).filter(
            CandidatoConocimiento.id_herramienta == id_herramienta
        )
    if id_habilidad_tecnica:
        query = query.join(Candidato.conocimientos).filter(
            CandidatoConocimiento.id_habilidad_tecnica == id_habilidad_tecnica
        )
    if id_titulo:
        query = query.join(Candidato.educaciones).filter(
            Educacion.id_titulo == id_titulo
        )
    if id_nivel_ingles:
        query = query.filter(
            Candidato.educaciones.any(Educacion.id_nivel_ingles == id_nivel_ingles)
        )

    if id_experiencia:
        query = query.join(Candidato.experiencias).filter(
            ExperienciaLaboral.id_rango_experiencia == id_experiencia
        )


#Esto es lo nuevo hasta antes del total
    if anio:
        query = query.filter(extract("year", Candidato.fecha_registro) == anio)

    if mes:
        query = query.filter(extract("month", Candidato.fecha_registro) == mes)


    if id_nivel_educacion:
        query = query.join(Candidato.educaciones).filter(
            Educacion.id_nivel_educacion == id_nivel_educacion
        )

    if id_habilidad_blanda:
        query = query.join(Candidato.conocimientos).filter(
            CandidatoConocimiento.id_habilidad_blanda == id_habilidad_blanda
        )

    if id_rango_salarial:
        query = query.join(Candidato.preferencias).filter(
            PreferenciaDisponibilidad.id_rango_salarial == id_rango_salarial
        )

    if ha_trabajado_joyco is not None:
        query = query.filter(Candidato.ha_trabajado_joyco == ha_trabajado_joyco)

    if tiene_referido is not None:
        query = query.filter(Candidato.tiene_referido == tiene_referido)

    if disponibilidad_viajar is not None:
        query = query.join(Candidato.preferencias).filter(
            PreferenciaDisponibilidad.disponibilidad_viajar == disponibilidad_viajar
        )

    if trabaja_actualmente is not None:
        query = query.join(Candidato.preferencias).filter(
            PreferenciaDisponibilidad.trabaja_actualmente == trabaja_actualmente
        )



    # Cálculo antes del paginado
    total = query.count()

    # Aplicar ordenamiento si se solicitó
    if ordenar_por_fecha == "recientes":
        query = query.order_by(desc(Candidato.fecha_registro))
    elif ordenar_por_fecha == "antiguos":
        query = query.order_by(Candidato.fecha_registro)

    # aplicar paginación
    candidatos = query.offset(skip).limit(limit).all()

    # Lógica para armar el resumen
    resumen = [mapear_candidato_resumen(c) for c in candidatos]

    # Retorno del total
    return {"data": resumen, "total": total}


# -------------Detalle de un Candidato -----------------#
def get_candidato_detalle(db: Session, id_candidato: int) -> CandidatoDetalleResponse:
    candidato = (
        db.query(Candidato)
        .options(
            joinedload(Candidato.ciudad).joinedload(Ciudad.departamento),
            joinedload(Candidato.cargo),
            joinedload(Candidato.centro_costos),
            joinedload(Candidato.motivo_salida),
            # Joins de Educación
            joinedload(Candidato.educaciones).joinedload(Educacion.nivel_educacion),
            joinedload(Candidato.educaciones).joinedload(Educacion.titulo),
            joinedload(Candidato.educaciones).joinedload(Educacion.institucion),
            joinedload(Candidato.educaciones).joinedload(Educacion.nivel_ingles),
            # Joins de Experiencia
            joinedload(Candidato.experiencias).joinedload(
                ExperienciaLaboral.rango_experiencia
            ),
            # Joins de Conocimientos
            joinedload(Candidato.conocimientos).joinedload(
                CandidatoConocimiento.habilidad_blanda
            ),
            joinedload(Candidato.conocimientos).joinedload(
                CandidatoConocimiento.habilidad_tecnica
            ),
            joinedload(Candidato.conocimientos).joinedload(
                CandidatoConocimiento.herramienta
            ),
            # Joins de Preferencias
            joinedload(Candidato.preferencias).joinedload(
                PreferenciaDisponibilidad.disponibilidad
            ),
            joinedload(Candidato.preferencias).joinedload(
                PreferenciaDisponibilidad.rango_salarial
            ),
            joinedload(Candidato.preferencias).joinedload(
                PreferenciaDisponibilidad.motivo_salida
            ),
        )
        .filter(Candidato.id_candidato == id_candidato)
        .first()
    )
    # Verifica si el candidato existe
    if not candidato:
        raise HTTPException(status_code=404, detail="Candidato no encontrado")
    return mapear_candidato_detalle(candidato)


def get_candidatos_detalle_lista(
    db: Session,
    search: str = None,
    estado: str = None,
    id_disponibilidad: int = None,
    id_cargo: int = None,
    id_ciudad: int = None,
    id_herramienta: int = None,
    id_habilidad_tecnica: int = None,
    id_nivel_ingles: int = None,
    id_experiencia: int = None,
    id_titulo: int = None,
    trabaja_joyco: bool = None,
    ordenar_por_fecha: Optional[str] = None,
    anio: Optional[int] = None,
    mes: Optional[int] = None,
    skip: int = 0,
    limit: int = 10,
    # Nuevos filtros
    id_nivel_educacion: int = None,
    id_habilidad_blanda: int = None,
    id_rango_salarial: int = None,
    ha_trabajado_joyco: bool = None,
    tiene_referido: bool = None,
    disponibilidad_viajar: bool = None,
    trabaja_actualmente: bool = None,
):
    query = db.query(Candidato).options(
        joinedload(Candidato.ciudad).joinedload(Ciudad.departamento),
        joinedload(Candidato.cargo),
        joinedload(Candidato.centro_costos),
        joinedload(Candidato.motivo_salida),
        joinedload(Candidato.educaciones).joinedload(Educacion.nivel_educacion),
        joinedload(Candidato.educaciones).joinedload(Educacion.titulo),
        joinedload(Candidato.educaciones).joinedload(Educacion.institucion),
        joinedload(Candidato.educaciones).joinedload(Educacion.nivel_ingles),
        joinedload(Candidato.experiencias).joinedload(
            ExperienciaLaboral.rango_experiencia
        ),
        joinedload(Candidato.conocimientos).joinedload(
            CandidatoConocimiento.habilidad_blanda
        ),
        joinedload(Candidato.conocimientos).joinedload(
            CandidatoConocimiento.habilidad_tecnica
        ),
        joinedload(Candidato.conocimientos).joinedload(
            CandidatoConocimiento.herramienta
        ),
        joinedload(Candidato.preferencias).joinedload(
            PreferenciaDisponibilidad.disponibilidad
        ),
        joinedload(Candidato.preferencias).joinedload(
            PreferenciaDisponibilidad.rango_salarial
        ),
        joinedload(Candidato.preferencias).joinedload(
            PreferenciaDisponibilidad.motivo_salida
        ),
    )

    # Filtros
    if search:
        query = query.join(Candidato.cargo).filter(
            or_(
                Candidato.nombre_completo.ilike(f"%{search}%"),
                Candidato.correo_electronico.ilike(f"%{search}%"),
                CargoOfrecido.nombre_cargo.ilike(f"%{search}%"),
            )
        )
    if estado:
        query = query.filter(Candidato.estado == estado)
        
    if id_disponibilidad:
        query = query.join(Candidato.preferencias).filter(
            PreferenciaDisponibilidad.id_disponibilidad_inicio == id_disponibilidad
        )

    if id_cargo:
        query = query.filter(Candidato.id_cargo == id_cargo)
    if id_ciudad:
        query = query.filter(Candidato.id_ciudad == id_ciudad)
    if trabaja_joyco is not None:
        query = query.filter(Candidato.trabaja_actualmente_joyco == trabaja_joyco)
    if id_herramienta:
        query = query.join(Candidato.conocimientos).filter(
            CandidatoConocimiento.id_herramienta == id_herramienta
        )
    if id_habilidad_tecnica:
        query = query.join(Candidato.conocimientos).filter(
            CandidatoConocimiento.id_habilidad_tecnica == id_habilidad_tecnica
        )
    if id_titulo:
        query = query.join(Candidato.educaciones).filter(
            Educacion.id_titulo == id_titulo
        )
    if id_nivel_ingles:
        query = query.filter(
            Candidato.educaciones.any(Educacion.id_nivel_ingles == id_nivel_ingles)
        )

    if id_experiencia:
        query = query.join(Candidato.experiencias).filter(
            ExperienciaLaboral.id_rango_experiencia == id_experiencia
        )
    if anio:
        query = query.filter(extract("year", Candidato.fecha_registro) == anio)
    if mes:
        query = query.filter(extract("month", Candidato.fecha_registro) == mes)



#Esto es lo nuevo hasta antes del total
    if anio:
        query = query.filter(extract("year", Candidato.fecha_registro) == anio)

    if mes:
        query = query.filter(extract("month", Candidato.fecha_registro) == mes)


    if id_nivel_educacion:
        query = query.join(Candidato.educaciones).filter(
            Educacion.id_nivel_educacion == id_nivel_educacion
        )

    if id_habilidad_blanda:
        query = query.join(Candidato.conocimientos).filter(
            CandidatoConocimiento.id_habilidad_blanda == id_habilidad_blanda
        )

    if id_rango_salarial:
        query = query.join(Candidato.preferencias).filter(
            PreferenciaDisponibilidad.id_rango_salarial == id_rango_salarial
        )

    if ha_trabajado_joyco is not None:
        query = query.filter(Candidato.ha_trabajado_joyco == ha_trabajado_joyco)

    if tiene_referido is not None:
        query = query.filter(Candidato.tiene_referido == tiene_referido)

    if disponibilidad_viajar is not None:
        query = query.join(Candidato.preferencias).filter(
            PreferenciaDisponibilidad.disponibilidad_viajar == disponibilidad_viajar
        )

    if trabaja_actualmente is not None:
        query = query.join(Candidato.preferencias).filter(
            PreferenciaDisponibilidad.trabaja_actualmente == trabaja_actualmente
        )









    total = query.count()

    if ordenar_por_fecha == "recientes":
        query = query.order_by(desc(Candidato.fecha_registro))
    elif ordenar_por_fecha == "antiguos":
        query = query.order_by(Candidato.fecha_registro)

    candidatos = query.offset(skip).limit(limit).all()
    data = [mapear_candidato_detalle(c) for c in candidatos]

    return {"data": data, "total": total}


def obtener_estadisticas_candidatos(db: Session) -> dict:
    resultados = (
        db.query(Candidato.estado, func.count(Candidato.id_candidato))
        .group_by(Candidato.estado)
        .all()
    )
    resumen = {estado: cantidad for estado, cantidad in resultados}
    resumen["total"] = sum(resumen.values())
    return resumen


def marcar_formulario_completo(db: Session, id_candidato: int) -> Candidato:
    candidato = (
        db.query(Candidato).filter(Candidato.id_candidato == id_candidato).first()
    )
    if not candidato:
        raise HTTPException(status_code=404, detail="Candidato no encontrado")

    candidato.formulario_completo = True
    db.commit()
    db.refresh(candidato)
    return candidato


def eliminar_candidatos_incompletos(db: Session) -> dict:
    limite = datetime.now(timezone.utc) - timedelta(hours=6)
    candidatos = (
        db.query(Candidato)
        .filter(
            Candidato.formulario_completo == False, Candidato.fecha_registro < limite
        )
        .all()
    )

    eliminados = 0
    for candidato in candidatos:
        db.delete(candidato)
        eliminados += 1

    db.commit()
    return {"eliminados": eliminados}
