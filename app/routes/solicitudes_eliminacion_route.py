from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional

from app.schemas.solicitud_eliminacion_schema import ConteoSolicitudesEliminacion, SolicitudEliminacionCreate, SolicitudEliminacionResponse, SolicitudesPaginadasResponse
from app.services.solicitudes_eliminacion_service import crear_solicitud_eliminacion, get_estadisticas_solicitudes_eliminacion, get_solicitudes_eliminacion, update_solicitud_eliminacion
from app.core.database import get_db

from fastapi import Path
from app.services.solicitudes_eliminacion_service import eliminar_solicitud_eliminacion

router = APIRouter(prefix="/solicitudes-eliminacion", tags=["Solicitudes de Eliminación"])


@router.get("/", response_model=SolicitudesPaginadasResponse)
def listar_solicitudes_eliminacion(
    search: Optional[str] = Query(None, description="Buscar por nombre, correo o cédula"),
    estado: Optional[str] = Query(None, description="pendiente, atendida o eliminada"),
    anio: Optional[int] = Query(None, alias="anio", description="Filtrar por año de solicitud"),
    mes: Optional[int] = Query(None, ge=1, le=12, description="Filtrar por mes (1-12)"),  # 👈 AÑADIDO
    ordenar_por_fecha: Optional[str] = Query(None, description="recientes o antiguos"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    db: Session = Depends(get_db)
):
    return get_solicitudes_eliminacion(
        db=db,
        search=search,
        estado=estado,
        año=anio,  # aquí lo pasas con el nombre correcto
        mes=mes,  # 👈 AÑADIDO
        ordenar_por_fecha=ordenar_por_fecha,
        skip=skip,
        limit=limit,
    )



@router.post("/", response_model=SolicitudEliminacionResponse, status_code=201)
def enviar_solicitud_eliminacion(
    data: SolicitudEliminacionCreate,
    db: Session = Depends(get_db)
):
    return crear_solicitud_eliminacion(db, data)


class ActualizacionSolicitudRequest(BaseModel):
    estado: str
    observacion_admin: Optional[str] = None


@router.put("/{id}", response_model=SolicitudEliminacionResponse)
def actualizar_solicitud(
    id: int,
    datos: ActualizacionSolicitudRequest,
    db: Session = Depends(get_db)
):
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
    return eliminar_solicitud_eliminacion(db, id)

@router.get("/estadisticas", response_model=ConteoSolicitudesEliminacion)
def obtener_estadisticas_solicitudes(
    año: Optional[int] = Query(None),
    mes: Optional[int] = Query(None, ge=1, le=12),  # 👈 AÑADIDO
    db: Session = Depends(get_db)
):
    return get_estadisticas_solicitudes_eliminacion(db, año=año, mes=mes)
