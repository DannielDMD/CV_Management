from datetime import datetime, timedelta, timezone
import logging
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.models.candidato_model import Candidato
from app.schemas.candidato_schema import (
    CandidatoCreate,
    CandidatoResponse,
    CandidatoUpdate,
    CandidatoResumenResponse,
)
from sqlalchemy.orm import Session, joinedload

from app.models.educacion_model import Educacion
from app.models.experiencia_model import ExperienciaLaboral
from app.models.conocimientos_model import CandidatoConocimiento
from app.models.preferencias import PreferenciaDisponibilidad

from sqlalchemy import desc, extract, func, or_
from app.models.catalogs.cargo_ofrecido import CargoOfrecido
from app.utils.orden_catalogos import ordenar_por_nombre


# Configurar logging
logger = logging.getLogger(__name__)


# Crear un candidato
def create_candidato(db: Session, candidato_data: CandidatoCreate):
    if (
        db.query(Candidato)
        .filter(Candidato.correo_electronico == candidato_data.correo_electronico)
        .first()
    ):
        raise HTTPException(
            status_code=400, detail="El correo electrónico ya está registrado"
        )

    nuevo_candidato = Candidato(**candidato_data.model_dump())

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


# Obtener un candidato por ID
def get_candidato_by_id(db: Session, id_candidato: int):
    candidato = db.get(Candidato, id_candidato)
    if not candidato:
        raise HTTPException(status_code=404, detail="Candidato no encontrado")
    return candidato


# Obtener todos los candidatos
def get_all_candidatos(db: Session):
    return db.query(Candidato).all()


# Actualizar un candidato
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


# Eliminar un candidato
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
    ordenar_por_fecha: Optional[str] = None,  # 👈 aquí lo agregamos
    skip: int = 0,
    limit: int = 10,
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

    # 👇 tus filtros
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
            PreferenciaDisponibilidad.id_disponibilidad == id_disponibilidad
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
        query = query.join(Candidato.educaciones).filter(
            Educacion.id_nivel_ingles == id_nivel_ingles
        )
    if id_experiencia:
        query = query.join(Candidato.experiencias).filter(
            ExperienciaLaboral.id_rango_experiencia == id_experiencia
        )

    # ✅ calculamos total antes del paginado
    total = query.count()

    # ✅ aplicar ordenamiento por fecha si se pidió
    if ordenar_por_fecha == "recientes":
        query = query.order_by(desc(Candidato.fecha_registro))
    elif ordenar_por_fecha == "antiguos":
        query = query.order_by(Candidato.fecha_registro)

    # ✅ aplicamos paginación
    candidatos = query.offset(skip).limit(limit).all()

    # 👇 tu lógica para armar el resumen
    resumen = []
    for candidato in candidatos:
        educacion = candidato.educaciones[0] if candidato.educaciones else None
        experiencia = candidato.experiencias[0] if candidato.experiencias else None
        preferencias = candidato.preferencias[0] if candidato.preferencias else None

        habilidades_blandas = []
        habilidades_tecnicas = []
        herramientas = []

        for c in candidato.conocimientos:
            if c.tipo_conocimiento == "blanda" and c.habilidad_blanda:
                habilidades_blandas.append(c.habilidad_blanda.nombre_habilidad_blanda)
            elif c.tipo_conocimiento == "tecnica" and c.habilidad_tecnica:
                habilidades_tecnicas.append(
                    c.habilidad_tecnica.nombre_habilidad_tecnica
                )
            elif c.tipo_conocimiento == "herramienta" and c.herramienta:
                herramientas.append(c.herramienta.nombre_herramienta)

        resumen.append(
            CandidatoResumenResponse(
                id_candidato=candidato.id_candidato,
                nombre_completo=candidato.nombre_completo,
                correo_electronico=candidato.correo_electronico,
                telefono=candidato.telefono,
                ciudad=candidato.ciudad.nombre_ciudad,
                cargo_ofrecido=candidato.cargo.nombre_cargo,
                nivel_educativo=(
                    educacion.nivel_educacion.descripcion_nivel if educacion else None
                ),
                titulo_obtenido=(
                    educacion.titulo.nombre_titulo
                    if educacion and educacion.titulo
                    else None
                ),
                rango_experiencia=(
                    experiencia.rango_experiencia.descripcion_rango
                    if experiencia
                    else None
                ),
                habilidades_blandas=habilidades_blandas,
                habilidades_tecnicas=habilidades_tecnicas,
                herramientas=herramientas,
                disponibilidad_inicio=(
                    preferencias.disponibilidad.descripcion_disponibilidad
                    if preferencias
                    else None
                ),
                trabaja_actualmente_joyco=candidato.trabaja_actualmente_joyco,
                fecha_postulacion=candidato.fecha_registro,
                estado=candidato.estado,
            )
        )

    # ✅ devolvemos también el total
    return {"data": resumen, "total": total}


# -------------Detalle de un Candidato -----------------#
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from app.models.candidato_model import Candidato
from app.schemas.candidato_schema import CandidatoDetalleResponse


def get_candidato_detalle(db: Session, id_candidato: int) -> CandidatoDetalleResponse:
    candidato = (
        db.query(Candidato)
        .options(
            joinedload(Candidato.ciudad),
            joinedload(Candidato.cargo),
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

    if not candidato:
        raise HTTPException(status_code=404, detail="Candidato no encontrado")

    educacion = candidato.educaciones[0] if candidato.educaciones else None
    experiencia = candidato.experiencias[0] if candidato.experiencias else None
    preferencias = candidato.preferencias[0] if candidato.preferencias else None

    habilidades_blandas = [
        c.habilidad_blanda.nombre_habilidad_blanda
        for c in candidato.conocimientos
        if c.tipo_conocimiento == "blanda" and c.habilidad_blanda
    ]
    habilidades_tecnicas = [
        c.habilidad_tecnica.nombre_habilidad_tecnica
        for c in candidato.conocimientos
        if c.tipo_conocimiento == "tecnica" and c.habilidad_tecnica
    ]
    herramientas = [
        c.herramienta.nombre_herramienta
        for c in candidato.conocimientos
        if c.tipo_conocimiento == "herramienta" and c.herramienta
    ]

    return CandidatoDetalleResponse(
        # 📌 Información Personal
        nombre_completo=candidato.nombre_completo,
        correo_electronico=candidato.correo_electronico,
        cc=candidato.cc,
        fecha_nacimiento=candidato.fecha_nacimiento,
        telefono=candidato.telefono,
        ciudad=candidato.ciudad.nombre_ciudad,
        descripcion_perfil=candidato.descripcion_perfil,
        cargo=candidato.cargo.nombre_cargo,
        trabaja_actualmente_joyco=candidato.trabaja_actualmente_joyco,
        ha_trabajado_joyco=candidato.ha_trabajado_joyco,
        motivo_salida=(
            candidato.motivo_salida.descripcion_motivo
            if candidato.motivo_salida
            else None
        ),
        tiene_referido=candidato.tiene_referido,
        nombre_referido=candidato.nombre_referido,
        fecha_registro=candidato.fecha_registro,
        estado=candidato.estado,
        # 🎓 Educación
        nivel_educacion=(
            educacion.nivel_educacion.descripcion_nivel if educacion else None
        ),
        titulo=(
            educacion.titulo.nombre_titulo if educacion and educacion.titulo else None
        ),
        institucion=(
            educacion.institucion.nombre_institucion
            if educacion and educacion.institucion
            else None
        ),
        anio_graduacion=educacion.anio_graduacion if educacion else None,
        nivel_ingles=educacion.nivel_ingles.nivel if educacion else None,
        # 💼 Experiencia
        rango_experiencia=(
            experiencia.rango_experiencia.descripcion_rango if experiencia else None
        ),
        ultima_empresa=experiencia.ultima_empresa if experiencia else None,
        ultimo_cargo=experiencia.ultimo_cargo if experiencia else None,
        funciones=experiencia.funciones if experiencia else None,
        fecha_inicio=experiencia.fecha_inicio if experiencia else None,
        fecha_fin=experiencia.fecha_fin if experiencia else None,
        # 🧠 Conocimientos
        habilidades_blandas=habilidades_blandas,
        habilidades_tecnicas=habilidades_tecnicas,
        herramientas=herramientas,
        # ⚙️ Preferencias
        disponibilidad_viajar=(
            preferencias.disponibilidad_viajar if preferencias else None
        ),
        disponibilidad_inicio=(
            preferencias.disponibilidad.descripcion_disponibilidad
            if preferencias
            else None
        ),
        rango_salarial=(
            preferencias.rango_salarial.descripcion_rango if preferencias else None
        ),
        trabaja_actualmente=preferencias.trabaja_actualmente if preferencias else None,
        motivo_salida_laboral=(
            preferencias.motivo_salida.descripcion_motivo
            if preferencias and preferencias.motivo_salida
            else None
        ),
        razon_trabajar_joyco=(
            preferencias.razon_trabajar_joyco if preferencias else None
        ),
    )


def obtener_estadisticas_candidatos(db: Session, año: Optional[int] = None):
    query = db.query(Candidato.estado, func.count(Candidato.id_candidato))
    if año:
        query = query.filter(extract("year", Candidato.fecha_registro) == año)
    
    resultados = query.group_by(Candidato.estado).all()

    resumen = {estado: cantidad for estado, cantidad in resultados}
    resumen["total"] = sum(resumen.values())
    return resumen

# NUEVA FUNCIÓN AGREGADA PARA SABER SI EL FORMULARIO SE COMPLETÓ
def marcar_formulario_completo(db: Session, id_candidato: int):
    candidato = db.query(Candidato).filter(Candidato.id_candidato == id_candidato).first()
    if not candidato:
        raise HTTPException(status_code=404, detail="Candidato no encontrado")

    candidato.formulario_completo = True
    db.commit()
    db.refresh(candidato)
    return candidato

#Función de Eliminación de Candidatos incompletos
def eliminar_candidatos_incompletos(db: Session):
    limite = datetime.now(timezone.utc) - timedelta(hours=6)
    candidatos = db.query(Candidato).filter(
        Candidato.formulario_completo == False,
        Candidato.fecha_registro < limite
    ).all()

    eliminados = 0
    for candidato in candidatos:
        db.delete(candidato)
        eliminados += 1

    db.commit()
    return {"eliminados": eliminados}
