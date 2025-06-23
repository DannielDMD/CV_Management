"""
Servicios para el catálogo de Títulos Obtenidos.
Incluye funciones CRUD: listar, obtener por ID, filtrar por nivel, crear, actualizar y eliminar.
"""

import math
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from app.models.catalogs.titulo import TituloObtenido
from app.schemas.catalogs.titulo import TituloObtenidoCreate, TituloObtenidoPaginatedResponse, TituloObtenidoUpdate
from app.utils.orden_catalogos import ordenar_por_nombre




def get_titulos(db: Session, skip: int = 0, limit: int = 100):
    query = db.query(TituloObtenido).options(joinedload(TituloObtenido.nivel_educacion))
    ordenado = ordenar_por_nombre(query, "nombre_titulo")
    return ordenado.offset(skip).limit(limit).all()

def get_titulo(db: Session, titulo_id: int):
    """
    Obtiene un título por su ID.
    """
    titulo = db.query(TituloObtenido).filter(TituloObtenido.id_titulo == titulo_id).first()
    if not titulo:
        raise HTTPException(status_code=404, detail="Título no encontrado")
    return titulo




def get_titulos_por_nivel(db: Session, id_nivel_educacion: int, skip: int = 0, limit: int = 100):
    query = db.query(TituloObtenido).options(joinedload(TituloObtenido.nivel_educacion)).filter(
        TituloObtenido.id_nivel_educacion == id_nivel_educacion
    )
    ordenado = ordenar_por_nombre(query, "nombre_titulo")
    return ordenado.offset(skip).limit(limit).all()


def get_titulos_con_filtros(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
    id_nivel_educacion: Optional[int] = None
) -> TituloObtenidoPaginatedResponse:
    """
    Retorna títulos con búsqueda, paginación y filtro por nivel educativo, incluyendo el nombre del nivel.
    """
    query = db.query(TituloObtenido).options(joinedload(TituloObtenido.nivel_educacion))

    if search:
        query = query.filter(TituloObtenido.nombre_titulo.ilike(f"%{search}%"))
    
    if id_nivel_educacion:
        query = query.filter(TituloObtenido.id_nivel_educacion == id_nivel_educacion)

    total = query.count()

    resultados = query.order_by(TituloObtenido.nombre_titulo.asc())\
        .offset(skip).limit(limit).all()

    page = (skip // limit) + 1 if limit > 0 else 1
    total_pages = math.ceil(total / limit) if limit > 0 else 1

    return TituloObtenidoPaginatedResponse(
        total=total,
        page=page,
        per_page=limit,
        total_pages=total_pages,
        resultados=resultados
    )




def create_titulo(db: Session, titulo: TituloObtenidoCreate):
    """
    Crea un nuevo título.
    """
    try:
        db_titulo = TituloObtenido(**titulo.model_dump())
        db.add(db_titulo)
        db.commit()
        db.refresh(db_titulo)
        return db_titulo
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el título: {str(e)}")


def update_titulo(db: Session, titulo_id: int, titulo_update: TituloObtenidoUpdate):
    """
    Actualiza los datos de un título existente.
    """
    db_titulo = db.query(TituloObtenido).filter(TituloObtenido.id_titulo == titulo_id).first()
    if not db_titulo:
        raise HTTPException(status_code=404, detail="Título no encontrado")
    
    try:
        for key, value in titulo_update.model_dump(exclude_unset=True).items():
            setattr(db_titulo, key, value)
        db.commit()
        db.refresh(db_titulo)
        return db_titulo
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el título: {str(e)}")


def delete_titulo(db: Session, titulo_id: int):
    """
    Elimina un título por su ID.
    """
    db_titulo = db.query(TituloObtenido).filter(TituloObtenido.id_titulo == titulo_id).first()
    if not db_titulo:
        raise HTTPException(status_code=404, detail="Título no encontrado")

    try:
        db.delete(db_titulo)
        db.commit()
        return {"message": "Título eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar el título: {str(e)}")
