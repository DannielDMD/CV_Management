"""Rutas para la gestión de candidatos, incluyendo creación, actualización, consulta, eliminación y estadísticas."""

from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.candidato_service import (
    create_candidato,
    eliminar_candidatos_incompletos,
    get_candidato_by_id,
    get_all_candidatos,
    get_candidato_detalle,
    get_candidatos_detalle_lista,
    marcar_formulario_completo,
    obtener_estadisticas_candidatos,
    update_candidato,
    delete_candidato,
    get_candidatos_resumen,
)

from app.schemas.candidato_schema import (
    CandidatoCreate,
    CandidatoDetalleResponse,
    CandidatoUpdate,
    CandidatoResponse,
    EstadisticasCandidatosResponse,
    CandidatoResumenPaginatedResponse,
)

router = APIRouter(prefix="/candidatos", tags=["Candidatos"])


@router.post("/", response_model=CandidatoResponse, status_code=status.HTTP_201_CREATED)
def create_candidato_endpoint(
    candidato_data: CandidatoCreate, db: Session = Depends(get_db)
):
    """
    Crea un nuevo candidato con la información básica.

    Returns:
        CandidatoResponse: Datos del candidato creado.
    """
    return create_candidato(db, candidato_data)


@router.get("/resumen", response_model=CandidatoResumenPaginatedResponse)
def obtener_resumen_candidatos(
    db: Session = Depends(get_db),
    search: str = Query(None),
    # Filtros para Infor Personal
    estado: str = Query(None),
    id_cargo: int = Query(None),
    id_ciudad: int = Query(None),
    trabaja_joyco: bool = Query(None),
    ha_trabajado_joyco: bool = Query(None),
    tiene_referido: bool = Query(None),
    # Filtros Para Educación
    id_nivel_educacion: int = Query(None),
    id_titulo: int = Query(None),
    id_nivel_ingles: int = Query(None),
    # Filtros Para Experiencia
    id_experiencia: int = Query(None),
    # Filtros Para Conocimientos
    id_habilidad_blanda: int = Query(None),
    id_habilidad_tecnica: int = Query(None),
    id_herramienta: int = Query(None),
    # Filtros Para Disponibilidad
    id_disponibilidad: int = Query(None),
    disponibilidad_viajar: bool = Query(None),
    trabaja_actualmente: bool = Query(None),
    id_rango_salarial: int = Query(None),
    ordenar_por_fecha: Optional[str] = Query(None),
    anio: Optional[int] = Query(None),
    mes: Optional[int] = Query(None, ge=1, le=12),
    skip: int = Query(0),
    limit: int = Query(10),
):
    """
    Devuelve un resumen paginado de candidatos con filtros por estado, cargo, ciudad, habilidades, etc.

    Returns:
        CandidatoResumenPaginatedResponse: Datos resumidos de los candidatos filtrados.
    """
    return get_candidatos_resumen(
        db=db,
        search=search,
        estado=estado,
        # Filtros por Info Personal}
        id_cargo=id_cargo,
        id_ciudad=id_ciudad,
        ha_trabajado_joyco=ha_trabajado_joyco,
        tiene_referido=tiene_referido,
        trabaja_joyco=trabaja_joyco,
        # Filtros por Educación
        id_nivel_educacion=id_nivel_educacion,
        id_titulo=id_titulo,
        id_nivel_ingles=id_nivel_ingles,
        # Filtros por Experiencia
        id_experiencia=id_experiencia,
        # Filtros por Conocimientos
        id_habilidad_tecnica=id_habilidad_tecnica,
        id_habilidad_blanda=id_habilidad_blanda,
        id_herramienta=id_herramienta,
        # Filtros por Disponibilidad
        id_disponibilidad=id_disponibilidad,
        id_rango_salarial=id_rango_salarial,
        disponibilidad_viajar=disponibilidad_viajar,
        trabaja_actualmente=trabaja_actualmente,
        ordenar_por_fecha=ordenar_por_fecha,
        anio=anio,
        mes=mes,
        skip=skip,
        limit=limit,
    )


@router.get("/{id_candidato}/detalle", response_model=CandidatoDetalleResponse)
def obtener_candidato_detalle(id_candidato: int, db: Session = Depends(get_db)):
    """
    Devuelve el detalle completo de un candidato por su ID.

    Returns:
        CandidatoDetalleResponse: Información completa del candidato.
    """
    return get_candidato_detalle(db, id_candidato)


@router.get("/detalle-lista")
def obtener_lista_detallada(
    db: Session = Depends(get_db),
    search: str = Query(None),
    # Filtros para Infor Personal
    estado: str = Query(None),
    id_cargo: int = Query(None),
    id_ciudad: int = Query(None),
    trabaja_joyco: bool = Query(None),
    ha_trabajado_joyco: bool = Query(None),
    tiene_referido: bool = Query(None),
    # Filtros Para Educación
    id_nivel_educacion: int = Query(None),
    id_titulo: int = Query(None),
    id_nivel_ingles: int = Query(None),
    # Filtros Para Experiencia
    id_experiencia: int = Query(None),
    # Filtros Para Conocimientos
    id_habilidad_blanda: int = Query(None),
    id_habilidad_tecnica: int = Query(None),
    id_herramienta: int = Query(None),
    # Filtros Para Disponibilidad
    id_disponibilidad: int = Query(None),
    disponibilidad_viajar: bool = Query(None),
    trabaja_actualmente: bool = Query(None),
    id_rango_salarial: int = Query(None),
    ordenar_por_fecha: Optional[str] = Query(None),
    anio: Optional[int] = Query(None),
    mes: Optional[int] = Query(None, ge=1, le=12),
    skip: int = Query(0),
    limit: int = Query(10),
):
    """
    Devuelve la lista paginada de candidatos con detalle completo, aplicando los mismos filtros que el resumen.
    """
    return get_candidatos_detalle_lista(
        db=db,
        search=search,
        estado=estado,
        # Filtros por Info Personal}
        id_cargo=id_cargo,
        id_ciudad=id_ciudad,
        ha_trabajado_joyco=ha_trabajado_joyco,
        tiene_referido=tiene_referido,
        trabaja_joyco=trabaja_joyco,
        # Filtros por Educación
        id_nivel_educacion=id_nivel_educacion,
        id_titulo=id_titulo,
        id_nivel_ingles=id_nivel_ingles,
        # Filtros por Experiencia
        id_experiencia=id_experiencia,
        # Filtros por Conocimientos
        id_habilidad_tecnica=id_habilidad_tecnica,
        id_habilidad_blanda=id_habilidad_blanda,
        id_herramienta=id_herramienta,
        # Filtros por Disponibilidad
        id_disponibilidad=id_disponibilidad,
        id_rango_salarial=id_rango_salarial,
        disponibilidad_viajar=disponibilidad_viajar,
        trabaja_actualmente=trabaja_actualmente,
        ordenar_por_fecha=ordenar_por_fecha,
        anio=anio,
        mes=mes,
        skip=skip,
        limit=limit,
    )


@router.get("/estadisticas", response_model=EstadisticasCandidatosResponse)
def estadisticas_candidatos(db: Session = Depends(get_db)):
    """
    Devuelve estadísticas globales de candidatos registrados.

    Returns:
        EstadisticasCandidatosResponse: Métricas generales del sistema.
    """
    return obtener_estadisticas_candidatos(db)


@router.get("/{id_candidato}", response_model=CandidatoResponse)
def get_candidato_by_id_endpoint(id_candidato: int, db: Session = Depends(get_db)):
    """
    Obtiene la información básica de un candidato por su ID.

    Returns:
        CandidatoResponse: Datos generales del candidato.
    """
    return get_candidato_by_id(db, id_candidato)


@router.get("/", response_model=list[CandidatoResponse])
def get_all_candidatos_endpoint(db: Session = Depends(get_db)):
    """
    Lista todos los candidatos registrados en el sistema.

    Returns:
        list[CandidatoResponse]: Lista completa sin filtros.
    """
    return get_all_candidatos(db)


@router.put("/{id_candidato}", response_model=CandidatoResponse)
def update_candidato_endpoint(
    id_candidato: int, candidato_data: CandidatoUpdate, db: Session = Depends(get_db)
):
    """
    Actualiza la información básica de un candidato existente.

    Returns:
        CandidatoResponse: Datos actualizados del candidato.
    """
    return update_candidato(db, id_candidato, candidato_data)


@router.delete("/{id_candidato}")
def delete_candidato_endpoint(id_candidato: int, db: Session = Depends(get_db)):
    """
    Elimina un candidato por su ID.

    Returns:
        dict: Mensaje de confirmación.
    """
    return delete_candidato(db, id_candidato)


@router.put("/{id_candidato}/completar", response_model=CandidatoResponse)
def marcar_formulario_completo_endpoint(
    id_candidato: int, db: Session = Depends(get_db)
):
    """
    Marca el formulario de un candidato como completo.

    Returns:
        CandidatoResponse: Candidato actualizado con `formulario_completo = True`.
    """
    return marcar_formulario_completo(db, id_candidato)


@router.delete("/limpiar-incompletos")
def limpiar_candidatos_incompletos(db: Session = Depends(get_db)):
    """
    Elimina del sistema todos los candidatos que no han completado el formulario.

    Returns:
        dict: Resultado de la operación (cantidad eliminada).
    """
    return eliminar_candidatos_incompletos(db)
