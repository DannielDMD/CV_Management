"""
Servicios para el manejo del catálogo de Instituciones Académicas.
Permite operaciones CRUD sobre la tabla `instituciones_academicas`.
"""

import math
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.catalogs.instituciones import InstitucionAcademica
from app.schemas.catalogs.instituciones import (
    InstitucionAcademicaCreate,
    InstitucionAcademicaPaginatedResponse,
    InstitucionAcademicaUpdate,
)
from app.utils.orden_catalogos import ordenar_por_nombre


def get_institucion(db: Session, institucion_id: int):
    """
    Obtiene una institución por su ID.

    Args:
        db (Session): Sesión de la base de datos.
        institucion_id (int): ID de la institución a buscar.

    Returns:
        InstitucionAcademica: Objeto institución encontrado.

    Raises:
        HTTPException: Si no se encuentra la institución.
    """
    institucion = (
        db.query(InstitucionAcademica)
        .filter(InstitucionAcademica.id_institucion == institucion_id)
        .first()
    )
    if not institucion:
        raise HTTPException(status_code=404, detail="Institución no encontrada")
    return institucion


def get_instituciones(db: Session, skip: int = 0, limit: int = 100):
    """
    Lista todas las instituciones académicas ordenadas alfabéticamente.

    Args:
        db (Session): Sesión de la base de datos.
        skip (int): Paginación inicial.
        limit (int): Límite de resultados.

    Returns:
        List[InstitucionAcademica]: Lista de instituciones.
    """
    query = db.query(InstitucionAcademica)
    ordenado = ordenar_por_nombre(query, "nombre_institucion")
    return ordenado.offset(skip).limit(limit).all()

# Servicio para Las instituciones paginadas
def get_instituciones_academicas_con_paginacion(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None
) -> InstitucionAcademicaPaginatedResponse:
    """
    Retorna Instituciones con búsqueda y paginación.
    """
    query = db.query(InstitucionAcademica)

    if search:
        query = query.filter(InstitucionAcademica.nombre_institucion.ilike(f"%{search}%"))

    total = query.count()

    resultados = query.order_by(InstitucionAcademica.nombre_institucion.asc())\
        .offset(skip).limit(limit).all()

    page = (skip // limit) + 1 if limit > 0 else 1
    total_pages = math.ceil(total / limit) if limit > 0 else 1

    return InstitucionAcademicaPaginatedResponse(
        total=total,
        page=page,
        per_page=limit,
        total_pages=total_pages,
        resultados=resultados
    )






def create_institucion(db: Session, institucion: InstitucionAcademicaCreate):
    """
    Crea una nueva institución académica.

    Args:
        db (Session): Sesión de la base de datos.
        institucion (InstitucionAcademicaCreate): Datos de entrada.

    Returns:
        InstitucionAcademica: Institución creada.

    Raises:
        HTTPException: En caso de error interno.
    """
    try:
        db_institucion = InstitucionAcademica(**institucion.model_dump())
        db.add(db_institucion)
        db.commit()
        db.refresh(db_institucion)
        return db_institucion
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al crear la institución: {str(e)}"
        )


def update_institucion(db: Session, institucion_id: int, institucion_update: InstitucionAcademicaUpdate):
    """
    Actualiza los datos de una institución por su ID.

    Args:
        db (Session): Sesión de la base de datos.
        institucion_id (int): ID del registro a modificar.
        institucion_update (InstitucionAcademicaUpdate): Nuevos datos.

    Returns:
        InstitucionAcademica: Registro actualizado.

    Raises:
        HTTPException: Si no se encuentra el registro o falla la actualización.
    """
    db_institucion = db.query(InstitucionAcademica).filter(
        InstitucionAcademica.id_institucion == institucion_id
    ).first()

    if not db_institucion:
        raise HTTPException(status_code=404, detail="Institución no encontrada")

    try:
        for key, value in institucion_update.model_dump(exclude_unset=True).items():
            setattr(db_institucion, key, value)
        db.commit()
        db.refresh(db_institucion)
        return db_institucion
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al actualizar la institución: {str(e)}"
        )


def delete_institucion(db: Session, institucion_id: int):
    """
    Elimina una institución por su ID.

    Args:
        db (Session): Sesión de la base de datos.
        institucion_id (int): ID de la institución a eliminar.

    Returns:
        dict: Mensaje de éxito.

    Raises:
        HTTPException: Si no se encuentra el registro o falla la eliminación.
    """
    db_institucion = db.query(InstitucionAcademica).filter(
        InstitucionAcademica.id_institucion == institucion_id
    ).first()

    if not db_institucion:
        raise HTTPException(status_code=404, detail="Institución no encontrada")

    try:
        db.delete(db_institucion)
        db.commit()
        return {"message": "Institución eliminada exitosamente"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al eliminar la institución: {str(e)}"
        )
