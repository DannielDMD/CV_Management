"""
Servicios para la gestión de conocimientos del candidato:
Habilidades blandas, técnicas y herramientas.
Incluye validación de errores y ordenamiento alfabético.
"""

import math
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

from app.models.conocimientos_model import HabilidadBlanda, HabilidadTecnica, Herramienta
from app.schemas.catalogs.conocimientos_schema import (
    HabilidadBlandaCreate,
    HabilidadBlandaPaginatedResponse,
    HabilidadBlandaResponse,
    HabilidadTecnicaCreate,
    HabilidadTecnicaPaginatedResponse,
    HabilidadTecnicaResponse,
    HerramientaCreate,
    HerramientaPaginatedResponse,
    HerramientaResponse,
)
from app.utils.orden_catalogos import ordenar_por_nombre


# ----------------------------
# Habilidad Blanda
# ----------------------------



def get_habilidades_blandas(db: Session):
    try:
        query = db.query(HabilidadBlanda)
        ordenado = ordenar_por_nombre(query, "nombre_habilidad_blanda").all()
        if not ordenado:
            raise HTTPException(status_code=404, detail="No se encontraron habilidades blandas")
        return [HabilidadBlandaResponse.model_validate(h) for h in ordenado]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener habilidades blandas: {str(e)}")




def get_habilidades_blandas_con_paginacion(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None
) -> HabilidadBlandaPaginatedResponse:
    query = db.query(HabilidadBlanda)

    if search:
        query = query.filter(HabilidadBlanda.nombre_habilidad_blanda.ilike(f"%{search}%"))

    total = query.count()
    resultados = query.order_by(HabilidadBlanda.nombre_habilidad_blanda.asc())\
        .offset(skip).limit(limit).all()

    page = (skip // limit) + 1 if limit > 0 else 1
    total_pages = math.ceil(total / limit) if limit > 0 else 1

    return HabilidadBlandaPaginatedResponse(
        total=total,
        page=page,
        per_page=limit,
        total_pages=total_pages,
        resultados=resultados
    )


def create_habilidad_blanda(db: Session, data: HabilidadBlandaCreate) -> HabilidadBlanda:
    existente = db.query(HabilidadBlanda).filter(
        HabilidadBlanda.nombre_habilidad_blanda.ilike(data.nombre_habilidad_blanda.strip())
    ).first()
    if existente:
        raise HTTPException(status_code=400, detail="Ya existe una habilidad blanda con ese nombre.")

    nueva = HabilidadBlanda(nombre_habilidad_blanda=data.nombre_habilidad_blanda.strip())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

#Actualizacion

def update_habilidad_blanda(db: Session, id_habilidad: int, data: HabilidadBlandaCreate) -> HabilidadBlanda:
    habilidad = db.query(HabilidadBlanda).filter(HabilidadBlanda.id_habilidad_blanda == id_habilidad).first()
    if not habilidad:
        raise HTTPException(status_code=404, detail="Habilidad blanda no encontrada.")

    duplicado = db.query(HabilidadBlanda).filter(
        HabilidadBlanda.nombre_habilidad_blanda.ilike(data.nombre_habilidad_blanda.strip()),
        HabilidadBlanda.id_habilidad_blanda != id_habilidad
    ).first()
    if duplicado:
        raise HTTPException(status_code=400, detail="Ya existe otra habilidad blanda con ese nombre.")

    habilidad.nombre_habilidad_blanda = data.nombre_habilidad_blanda.strip()
    db.commit()
    db.refresh(habilidad)
    return habilidad

# Eliminación 

def delete_habilidad_blanda(db: Session, id_habilidad: int) -> bool:
    habilidad = db.query(HabilidadBlanda).filter(HabilidadBlanda.id_habilidad_blanda == id_habilidad).first()
    if not habilidad:
        raise HTTPException(status_code=404, detail="Habilidad blanda no encontrada.")

    db.delete(habilidad)
    db.commit()
    return {"message": "Habilidad blanda eliminada correctamente"}



# ----------------------------
# Habilidad Técnica
# ----------------------------

def get_habilidades_tecnicas(db: Session):
    try:
        query = db.query(HabilidadTecnica)
        ordenado = ordenar_por_nombre(query, "nombre_habilidad_tecnica").all()
        if not ordenado:
            raise HTTPException(status_code=404, detail="No se encontraron habilidades técnicas")
        return [HabilidadTecnicaResponse.model_validate(h) for h in ordenado]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener habilidades técnicas: {str(e)}")


#Lectura
def get_habilidades_tecnicas_con_paginacion(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None
) -> HabilidadTecnicaPaginatedResponse:
    query = db.query(HabilidadTecnica)

    if search:
        query = query.filter(HabilidadTecnica.nombre_habilidad_tecnica.ilike(f"%{search}%"))

    total = query.count()
    resultados = query.order_by(HabilidadTecnica.nombre_habilidad_tecnica.asc())\
        .offset(skip).limit(limit).all()

    page = (skip // limit) + 1 if limit > 0 else 1
    total_pages = math.ceil(total / limit) if limit > 0 else 1

    return HabilidadTecnicaPaginatedResponse(
        total=total,
        page=page,
        per_page=limit,
        total_pages=total_pages,
        resultados=resultados
    )

#Creacion
def create_habilidad_tecnica(db: Session, data: HabilidadTecnicaCreate) -> HabilidadTecnica:
    existente = db.query(HabilidadTecnica).filter(
        HabilidadTecnica.nombre_habilidad_tecnica.ilike(data.nombre_habilidad_tecnica.strip())
    ).first()
    if existente:
        raise HTTPException(status_code=400, detail="Ya existe una habilidad técnica con ese nombre.")

    nueva = HabilidadTecnica(nombre_habilidad_tecnica=data.nombre_habilidad_tecnica.strip())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

#Actualizacion
def update_habilidad_tecnica(db: Session, id_habilidad: int, data: HabilidadTecnicaCreate) -> HabilidadTecnica:
    habilidad = db.query(HabilidadTecnica).filter(HabilidadTecnica.id_habilidad_tecnica == id_habilidad).first()
    if not habilidad:
        raise HTTPException(status_code=404, detail="Habilidad técnica no encontrada.")

    duplicado = db.query(HabilidadTecnica).filter(
        HabilidadTecnica.nombre_habilidad_tecnica.ilike(data.nombre_habilidad_tecnica.strip()),
        HabilidadTecnica.id_habilidad_tecnica != id_habilidad
    ).first()
    if duplicado:
        raise HTTPException(status_code=400, detail="Ya existe otra habilidad técnica con ese nombre.")

    habilidad.nombre_habilidad_tecnica = data.nombre_habilidad_tecnica.strip()
    db.commit()
    db.refresh(habilidad)
    return habilidad

#Eliminacion
def delete_habilidad_tecnica(db: Session, id_habilidad: int) -> bool:
    habilidad = db.query(HabilidadTecnica).filter(HabilidadTecnica.id_habilidad_tecnica == id_habilidad).first()
    if not habilidad:
        raise HTTPException(status_code=404, detail="Habilidad técnica no encontrada.")

    db.delete(habilidad)
    db.commit()
    return True



# ----------------------------
# Herramienta
# ----------------------------
def get_herramientas(db: Session):
    try:
        query = db.query(Herramienta)
        ordenado = ordenar_por_nombre(query, "nombre_herramienta").all()
        if not ordenado:
            raise HTTPException(status_code=404, detail="No se encontraron herramientas")
        return [HerramientaResponse.model_validate(h) for h in ordenado]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener herramientas: {str(e)}")



def get_herramientas_con_paginacion(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None
) -> HerramientaPaginatedResponse:
    query = db.query(Herramienta)

    if search:
        query = query.filter(Herramienta.nombre_herramienta.ilike(f"%{search}%"))

    total = query.count()
    resultados = query.order_by(Herramienta.nombre_herramienta.asc())\
        .offset(skip).limit(limit).all()

    page = (skip // limit) + 1 if limit > 0 else 1
    total_pages = math.ceil(total / limit) if limit > 0 else 1

    return HerramientaPaginatedResponse(
        total=total,
        page=page,
        per_page=limit,
        total_pages=total_pages,
        resultados=resultados
    )
#ACreación
def create_herramienta(db: Session, data: HerramientaCreate) -> Herramienta:
    existente = db.query(Herramienta).filter(
        Herramienta.nombre_herramienta.ilike(data.nombre_herramienta.strip())
    ).first()
    if existente:
        raise HTTPException(status_code=400, detail="Ya existe una herramienta con ese nombre.")

    nueva = Herramienta(nombre_herramienta=data.nombre_herramienta.strip())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva
#Actualizacion
def update_herramienta(db: Session, id_herramienta: int, data: HerramientaCreate) -> Herramienta:
    herramienta = db.query(Herramienta).filter(Herramienta.id_herramienta == id_herramienta).first()
    if not herramienta:
        raise HTTPException(status_code=404, detail="Herramienta no encontrada.")

    duplicado = db.query(Herramienta).filter(
        Herramienta.nombre_herramienta.ilike(data.nombre_herramienta.strip()),
        Herramienta.id_herramienta != id_herramienta
    ).first()
    if duplicado:
        raise HTTPException(status_code=400, detail="Ya existe otra herramienta con ese nombre.")

    herramienta.nombre_herramienta = data.nombre_herramienta.strip()
    db.commit()
    db.refresh(herramienta)
    return herramienta

#Eliminacion
def delete_herramienta(db: Session, id_herramienta: int) -> bool:
    herramienta = db.query(Herramienta).filter(Herramienta.id_herramienta == id_herramienta).first()
    if not herramienta:
        raise HTTPException(status_code=404, detail="Herramienta no encontrada.")

    db.delete(herramienta)
    db.commit()
    return True
