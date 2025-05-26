"""Rutas para la gestión y administración de solicitudes de eliminación de datos personales."""

from fastapi import APIRouter, Depends, Query, Path
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.schemas.solicitud_eliminacion_schema import (
    SolicitudEliminacionCreate,
    SolicitudEliminacionResponse,
    SolicitudesPaginadasResponse,
    ConteoSolicitudesEliminacion
)
from app.services.solicitudes_eliminacion_service import (
    crear_solicitud_eliminacion,
    get_solicitudes_eliminacion,
    update_solicitud_eliminacion,
    eliminar_solicitud_eliminacion,
    get_estadisticas_solicitudes_eliminacion
)

router = APIRouter(prefix="/solicitudes-eliminacion", tags=["Solicitudes de Eliminación"])


@router.get("/", response_model=SolicitudesPaginadasResponse)
def listar_solicitudes_eliminacion(
    search: Optional[str] = Query(None, description="Buscar por nombre, correo o cédula"),
    estado: Optional[str] = Query(None, description="Estado de la solicitud: pendiente, atendida o eliminada"),
    anio: Optional[int] = Query(None, alias="anio", description="Filtrar por año de la solicitud"),
    mes: Optional[int] = Query(None, ge=1, le=12, description="Filtrar por mes (1-12)"),
    ordenar_por_fecha: Optional[str] = Query(None, description="Ordenar por fecha: recientes o antiguos"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    db: Session = Depends(get_db)
):
    """
    Lista las solicitudes de eliminación con filtros y paginación.

    Args:
        search (str, opcional): Filtro de búsqueda.
        estado (str, opcional): Estado de la solicitud.
        anio (int, opcional): Año de la solicitud.
        mes (int, opcional): Mes de la solicitud.
        ordenar_por_fecha (str, opcional): Ordenamiento por fecha.
        skip (int): Índice de paginación.
        limit (int): Límite de resultados.
        db (Session): Sesión de base de datos.

    Returns:
        SolicitudesPaginadasResponse: Lista paginada de solicitudes.
    """
    return get_solicitudes_eliminacion(
        db=db,
        search=search,
        estado=estado,
        año=anio,
        mes=mes,
        ordenar_por_fecha=ordenar_por_fecha,
        skip=skip,
        limit=limit,
    )


@router.post("/", response_model=SolicitudEliminacionResponse, status_code=201)
def enviar_solicitud_eliminacion(
    data: SolicitudEliminacionCreate,
    db: Session = Depends(get_db)
):
    """
    Crea una nueva solicitud de eliminación de datos personales.

    Args:
        data (SolicitudEliminacionCreate): Datos de la solicitud.
        db (Session): Sesión de base de datos.

    Returns:
        SolicitudEliminacionResponse: Solicitud creada.
    """
    return crear_solicitud_eliminacion(db, data)


class ActualizacionSolicitudRequest(BaseModel):
    """
    Modelo para actualizar el estado y observación de una solicitud.
    """
    estado: str
    observacion_admin: Optional[str] = None


@router.put("/{id}", response_model=SolicitudEliminacionResponse)
def actualizar_solicitud(
    id: int,
    datos: ActualizacionSolicitudRequest,
    db: Session = Depends(get_db)
):
    """
    Actualiza el estado y/o la observación administrativa de una solicitud.

    Args:
        id (int): ID de la solicitud.
        datos (ActualizacionSolicitudRequest): Datos a actualizar.
        db (Session): Sesión de base de datos.

    Returns:
        SolicitudEliminacionResponse: Solicitud actualizada.
    """
    return update_solicitud_eliminacion(
        db=db,
        id=id,
        nuevo_estado=datos.estado,
        observacion_admin=datos.observacion_admin
    )


@router.delete("/{id}", status_code=200)
def eliminar_solicitud(
    id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    """
    Elimina una solicitud de eliminación por su ID.

    Args:
        id (int): ID de la solicitud.
        db (Session): Sesión de base de datos.

    Returns:
        dict: Resultado de la operación.
    """
    return eliminar_solicitud_eliminacion(db, id)


@router.get("/estadisticas", response_model=ConteoSolicitudesEliminacion)
def obtener_estadisticas_solicitudes(
    año: Optional[int] = Query(None),
    mes: Optional[int] = Query(None, ge=1, le=12),
    db: Session = Depends(get_db)
):
    """
    Devuelve estadísticas de solicitudes agrupadas por estado.

    Args:
        año (int, opcional): Año para filtrar.
        mes (int, opcional): Mes para filtrar.
        db (Session): Sesión de base de datos.

    Returns:
        ConteoSolicitudesEliminacion: Conteo por estado.
    """
    return get_estadisticas_solicitudes_eliminacion(db, año=año, mes=mes)
