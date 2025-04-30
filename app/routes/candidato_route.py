from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.services.candidato_service import (
    create_candidato,
    eliminar_candidatos_incompletos,
    get_candidato_by_id,
    get_all_candidatos,
    get_candidato_detalle,
    marcar_formulario_completo,
    obtener_estadisticas_candidatos,
    update_candidato,
    delete_candidato,
)
from app.schemas.candidato_schema import (
    CandidatoCreate,
    CandidatoDetalleResponse,
    CandidatoUpdate,
    CandidatoResponse,
    EstadisticasCandidatosResponse,
)
from app.core.database import get_db
from app.services.candidato_service import get_candidatos_resumen
from app.schemas.candidato_schema import CandidatoResumenResponse
from app.schemas.candidato_schema import CandidatoResumenPaginatedResponse


router = APIRouter(prefix="/candidatos", tags=["Candidatos"])


# Crear un candidato
@router.post("/", response_model=CandidatoResponse, status_code=status.HTTP_201_CREATED)
def create_candidato_endpoint(
    candidato_data: CandidatoCreate, db: Session = Depends(get_db)
):
    return create_candidato(db, candidato_data)


@router.get("/resumen", response_model=CandidatoResumenPaginatedResponse)
def obtener_resumen_candidatos(
    db: Session = Depends(get_db),
    search: str = Query(None),
    estado: str = Query(None),
    id_disponibilidad: int = Query(None),
    id_cargo: int = Query(None),
    id_ciudad: int = Query(None),
    id_herramienta: int = Query(None),
    id_habilidad_tecnica: int = Query(None),
    id_nivel_ingles: int = Query(None),
    id_experiencia: int = Query(None),
    id_titulo: int = Query(None),
    trabaja_joyco: bool = Query(None),
    ordenar_por_fecha: Optional[str] = Query(None),
    skip: int = Query(0),
    limit: int = Query(10),
):
    return get_candidatos_resumen(
        db=db,
        search=search,
        estado=estado,
        id_disponibilidad=id_disponibilidad,
        id_cargo=id_cargo,
        id_ciudad=id_ciudad,
        id_herramienta=id_herramienta,
        id_habilidad_tecnica=id_habilidad_tecnica,
        id_nivel_ingles=id_nivel_ingles,
        id_experiencia=id_experiencia,
        id_titulo=id_titulo,
        trabaja_joyco=trabaja_joyco,
        ordenar_por_fecha=ordenar_por_fecha,
        skip=skip,
        limit=limit,
    )


# Obtener las generalidades de un candidato
@router.get("/{id_candidato}/detalle", response_model=CandidatoDetalleResponse)
def obtener_candidato_detalle(id_candidato: int, db: Session = Depends(get_db)):
    return get_candidato_detalle(db, id_candidato)


@router.get("/estadisticas", response_model=EstadisticasCandidatosResponse)
def estadisticas_candidatos(db: Session = Depends(get_db)):
    return obtener_estadisticas_candidatos(db)


# Obtener un candidato por ID
@router.get("/{id_candidato}", response_model=CandidatoResponse)
def get_candidato_by_id_endpoint(id_candidato: int, db: Session = Depends(get_db)):
    return get_candidato_by_id(db, id_candidato)


# Obtener todos los candidatos
@router.get("/", response_model=list[CandidatoResponse])
def get_all_candidatos_endpoint(db: Session = Depends(get_db)):
    return get_all_candidatos(db)


# Actualizar un candidato
@router.put("/{id_candidato}", response_model=CandidatoResponse)
def update_candidato_endpoint(
    id_candidato: int, candidato_data: CandidatoUpdate, db: Session = Depends(get_db)
):
    return update_candidato(db, id_candidato, candidato_data)


# Eliminar un candidato
@router.delete("/{id_candidato}")
def delete_candidato_endpoint(id_candidato: int, db: Session = Depends(get_db)):
    return delete_candidato(db, id_candidato)

# FUNCIÓN DEL ROUTE PARA CUANDO SE COMPLETÓ EL FORMULARIO
@router.put("/{id_candidato}/completar", response_model=CandidatoResponse)
def marcar_formulario_completo_endpoint(id_candidato: int, db: Session = Depends(get_db)):
    return marcar_formulario_completo(db, id_candidato)

# FUNCIÓN DE LA RUTA QUE ELIMINA LOS CANDIDATOS INCOMPLETOS
@router.delete("/limpiar-incompletos")
def limpiar_candidatos_incompletos(db: Session = Depends(get_db)):
    return eliminar_candidatos_incompletos(db)
