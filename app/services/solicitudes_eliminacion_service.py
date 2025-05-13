from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_, func, extract, desc
from app.models.solicitud_eliminacion_model import SolicitudEliminacion
from app.schemas.solicitud_eliminacion_schema import (
    SolicitudEliminacionCreate,
    SolicitudesPaginadasResponse,
    SolicitudEliminacionResponse,
)


def get_solicitudes_eliminacion(
    db: Session,
    search: str = None,
    estado: str = None,
    año: int = None,
    ordenar_por_fecha: str = None,
    skip: int = 0,
    limit: int = 10,
) -> SolicitudesPaginadasResponse:

    query = db.query(SolicitudEliminacion)

    # 🔍 Filtros
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
        query = query.filter(
            extract("year", SolicitudEliminacion.fecha_solicitud) == año
        )

    # 📅 Orden por fecha
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
    nueva_solicitud = SolicitudEliminacion(**data.model_dump())
    db.add(nueva_solicitud)
    db.commit()
    db.refresh(nueva_solicitud)
    return nueva_solicitud


def update_solicitud_eliminacion(
    db: Session, id: int, nuevo_estado: str, observacion_admin: str = None
) -> SolicitudEliminacionResponse:
    solicitud = (
        db.query(SolicitudEliminacion).filter(SolicitudEliminacion.id == id).first()
    )

    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")

    solicitud.estado = nuevo_estado
    if observacion_admin is not None:
        solicitud.observacion_admin = observacion_admin


    try:
        db.commit()
        db.refresh(solicitud)
        return solicitud
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al actualizar la solicitud")
