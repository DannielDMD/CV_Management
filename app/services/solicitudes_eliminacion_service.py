from typing import Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_, func, extract, desc
from app.models.solicitud_eliminacion_model import SolicitudEliminacion
from app.schemas.candidato_schema import EliminacionCandidatosResponse
from app.schemas.solicitud_eliminacion_schema import (
    ConteoSolicitudesEliminacion,
    SolicitudEliminacionCreate,
    SolicitudEliminacionLoteRequest,
    SolicitudesPaginadasResponse,
    SolicitudEliminacionResponse,
)

# ─────────────────────────────────────────────────────────────────────────────
# SERVICIO: Gestión de solicitudes de eliminación de datos personales
# Este servicio permite crear, listar, actualizar, eliminar y obtener estadísticas
# de las solicitudes hechas por los usuarios conforme a la Ley de Protección de Datos.
# ─────────────────────────────────────────────────────────────────────────────


def get_solicitudes_eliminacion(
    db: Session,
    search: str = None,
    estado: str = None,
    año: int = None,
    mes: int = None,
    ordenar_por_fecha: str = None,
    skip: int = 0,
    limit: int = 10,
) -> SolicitudesPaginadasResponse:
    """
    Retorna una lista paginada de solicitudes de eliminación, aplicando filtros opcionales.

    Args:
        db (Session): Sesión de base de datos.
        search (str, optional): Buscar por nombre, cédula o correo.
        estado (str, optional): Estado de la solicitud ("Pendiente", "Aceptada", "Rechazada").
        año (int, optional): Año de la solicitud.
        mes (int, optional): Mes de la solicitud.
        ordenar_por_fecha (str, optional): "recientes" o "antiguos".
        skip (int): Registros a omitir (paginación).
        limit (int): Cantidad de registros a retornar.

    Returns:
        SolicitudesPaginadasResponse: Resultado con data y total.
    """
    query = db.query(SolicitudEliminacion)

    if search:
        query = query.filter(
            or_(
                SolicitudEliminacion.nombre_completo.ilike(f"%{search}%"),
                SolicitudEliminacion.correo.ilike(f"%{search}%"),
                SolicitudEliminacion.cc.ilike(f"%{search}%"),
            )
        )
    if estado:
        query = query.filter(SolicitudEliminacion.estado == estado)
    if año:
        query = query.filter(extract("year", SolicitudEliminacion.fecha_solicitud) == año)
    if mes:
        query = query.filter(extract("month", SolicitudEliminacion.fecha_solicitud) == mes)
    if ordenar_por_fecha == "recientes":
        query = query.order_by(SolicitudEliminacion.fecha_solicitud.desc())
    elif ordenar_por_fecha == "antiguos":
        query = query.order_by(SolicitudEliminacion.fecha_solicitud.asc())

    total = query.count()
    resultados = query.offset(skip).limit(limit).all()

    return SolicitudesPaginadasResponse(
        data=[SolicitudEliminacionResponse.model_validate(r) for r in resultados],
        total=total,
    )


def crear_solicitud_eliminacion(
    db: Session, data: SolicitudEliminacionCreate
) -> SolicitudEliminacionResponse:
    """
    Crea una nueva solicitud de eliminación.

    Args:
        db (Session): Sesión de base de datos.
        data (SolicitudEliminacionCreate): Datos del formulario enviado por el usuario.

    Returns:
        SolicitudEliminacionResponse: Solicitud creada.
    """
    nueva_solicitud = SolicitudEliminacion(**data.model_dump())
    db.add(nueva_solicitud)
    db.commit()
    db.refresh(nueva_solicitud)
    return nueva_solicitud


def update_solicitud_eliminacion(
    db: Session, id: int, nuevo_estado: str, observacion_admin: str = None
) -> SolicitudEliminacionResponse:
    """
    Actualiza el estado de una solicitud (por ejemplo: Pendiente → Aceptada).

    Args:
        db (Session): Sesión de base de datos.
        id (int): ID de la solicitud.
        nuevo_estado (str): Nuevo estado ("Pendiente", "Aceptada", "Rechazada").
        observacion_admin (str, optional): Comentario adicional del administrador.

    Returns:
        SolicitudEliminacionResponse: Solicitud actualizada.
    """
    solicitud = db.query(SolicitudEliminacion).filter(SolicitudEliminacion.id == id).first()
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")

    solicitud.estado = nuevo_estado
    if observacion_admin is not None:
        solicitud.observacion_admin = observacion_admin

    try:
        db.commit()
        db.refresh(solicitud)
        return solicitud
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al actualizar la solicitud")


def eliminar_solicitud_eliminacion(db: Session, id: int):
    """
    Elimina una solicitud del sistema.

    Args:
        db (Session): Sesión de base de datos.
        id (int): ID de la solicitud.

    Returns:
        dict: Mensaje de confirmación.
    """
    solicitud = db.query(SolicitudEliminacion).filter(SolicitudEliminacion.id == id).first()
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")

    try:
        db.delete(solicitud)
        db.commit()
        return {"mensaje": "Solicitud eliminada"}
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al eliminar la solicitud")
    
def eliminar_solicitudes_por_lote(
    db: Session, payload: SolicitudEliminacionLoteRequest
) -> EliminacionCandidatosResponse:
    if not payload.ids:
        raise HTTPException(status_code=400, detail="La lista de solicitudes está vacía.")

    eliminados = []
    for id_solicitud in payload.ids:
        solicitud = db.query(SolicitudEliminacion).filter(SolicitudEliminacion.id == id_solicitud).first()
        if solicitud:
            db.delete(solicitud)
            eliminados.append(id_solicitud)

    if not eliminados:
        raise HTTPException(status_code=404, detail="No se encontró ninguna solicitud válida para eliminar.")

    try:
        db.commit()
        return EliminacionCandidatosResponse(eliminados=len(eliminados), detalles=eliminados)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al eliminar las solicitudes.")

def get_estadisticas_solicitudes_eliminacion(
    db: Session,
    año: Optional[int] = None,
    mes: Optional[int] = None
) -> ConteoSolicitudesEliminacion:
    """
    Devuelve estadísticas generales de las solicitudes, incluyendo conteos por estado
    y motivos, con posibilidad de filtrar por año y mes.

    Args:
        db (Session): Sesión de base de datos.
        año (int, optional): Año a filtrar.
        mes (int, optional): Mes a filtrar.

    Returns:
        ConteoSolicitudesEliminacion: Objeto con totales y subtotales.
    """
    query = db.query(SolicitudEliminacion)

    if año:
        query = query.filter(extract("year", SolicitudEliminacion.fecha_solicitud) == año)
    if mes:
        query = query.filter(extract("month", SolicitudEliminacion.fecha_solicitud) == mes)

    total = query.count()
    pendientes = query.filter(SolicitudEliminacion.estado == "Pendiente").count()
    rechazadas = query.filter(SolicitudEliminacion.estado == "Rechazada").count()
    aceptadas = query.filter(SolicitudEliminacion.estado == "Aceptada").count()
    motivo_actualizar = query.filter(SolicitudEliminacion.motivo.ilike("%actualizar%")).count()
    motivo_eliminar = query.filter(SolicitudEliminacion.motivo.ilike("%eliminar%")).count()

    return ConteoSolicitudesEliminacion(
        total=total,
        pendientes=pendientes,
        rechazadas=rechazadas,
        aceptadas=aceptadas,
        motivo_actualizar_datos=motivo_actualizar,
        motivo_eliminar_candidatura=motivo_eliminar,
    )
