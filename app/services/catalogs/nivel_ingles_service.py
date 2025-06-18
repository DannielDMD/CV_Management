"""
Servicios para el manejo del catálogo de Niveles de Inglés.
Incluye operaciones CRUD: listar, obtener, crear, actualizar y eliminar.
"""

import math
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.catalogs.nivel_ingles import NivelIngles
from app.schemas.catalogs.nivel_ingles import NivelInglesCreate, NivelInglesPaginatedResponse, NivelInglesUpdate


def get_niveles_ingles(db: Session):
    """
    Lista todos los niveles de inglés.

    Args:
        db (Session): Sesión activa de la base de datos.

    Returns:
        List[NivelIngles]: Lista de niveles.
    """
    return db.query(NivelIngles).all()


def get_nivel_ingles(db: Session, nivel_ingles_id: int):
    """
    Obtiene un nivel de inglés por su ID.

    Args:
        db (Session): Sesión activa de la base de datos.
        nivel_ingles_id (int): ID del nivel a consultar.

    Returns:
        NivelIngles: Objeto encontrado.

    Raises:
        HTTPException: Si no se encuentra el nivel.
    """
    nivel_ingles = db.query(NivelIngles).filter(
        NivelIngles.id_nivel_ingles == nivel_ingles_id
    ).first()

    if not nivel_ingles:
        raise HTTPException(status_code=404, detail="Nivel de inglés no encontrado")

    return nivel_ingles


#Servicio para la paginacion
def get_nivel_ingles_con_paginacion(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None
) -> NivelInglesPaginatedResponse:
    """
    Retorna centros de costos con búsqueda y paginación.
    """
    query = db.query(NivelIngles)

    if search:
        query = query.filter(NivelIngles.nivel.ilike(f"%{search}%"))

    total = query.count()

    resultados = query.order_by(NivelIngles.nivel.asc())\
        .offset(skip).limit(limit).all()

    page = (skip // limit) + 1 if limit > 0 else 1
    total_pages = math.ceil(total / limit) if limit > 0 else 1

    return NivelInglesPaginatedResponse(
        total=total,
        page=page,
        per_page=limit,
        total_pages=total_pages,
        resultados=resultados
    )



def create_nivel_ingles(db: Session, nivel_ingles_data: NivelInglesCreate):
    """
    Crea un nuevo nivel de inglés si no existe uno con el mismo nombre.

    Args:
        db (Session): Sesión activa de la base de datos.
        nivel_ingles_data (NivelInglesCreate): Datos del nuevo nivel.

    Returns:
        NivelIngles: Objeto creado.

    Raises:
        HTTPException: Si el nivel ya existe.
    """
    existe = db.query(NivelIngles).filter(
        NivelIngles.nivel == nivel_ingles_data.nivel
    ).first()
    if existe:
        raise HTTPException(status_code=400, detail="El nivel de inglés ya existe")

    nuevo_nivel = NivelIngles(nivel=nivel_ingles_data.nivel)
    db.add(nuevo_nivel)
    db.commit()
    db.refresh(nuevo_nivel)
    return nuevo_nivel


def update_nivel_ingles(db: Session, nivel_ingles_id: int, nivel_ingles_data: NivelInglesUpdate):
    """
    Actualiza el nombre de un nivel de inglés por ID.

    Args:
        db (Session): Sesión activa de la base de datos.
        nivel_ingles_id (int): ID del nivel a actualizar.
        nivel_ingles_data (NivelInglesUpdate): Datos actualizados.

    Returns:
        NivelIngles: Nivel actualizado.

    Raises:
        HTTPException: Si no se encuentra el nivel.
    """
    nivel_ingles = db.query(NivelIngles).filter(
        NivelIngles.id_nivel_ingles == nivel_ingles_id
    ).first()
    if not nivel_ingles:
        raise HTTPException(status_code=404, detail="Nivel de inglés no encontrado")

    nivel_ingles.nivel = nivel_ingles_data.nivel
    db.commit()
    db.refresh(nivel_ingles)
    return nivel_ingles


def delete_nivel_ingles(db: Session, nivel_ingles_id: int):
    """
    Elimina un nivel de inglés por su ID.

    Args:
        db (Session): Sesión activa de la base de datos.
        nivel_ingles_id (int): ID del nivel a eliminar.

    Returns:
        dict: Mensaje de confirmación.

    Raises:
        HTTPException: Si no se encuentra el nivel.
    """
    nivel_ingles = db.query(NivelIngles).filter(
        NivelIngles.id_nivel_ingles == nivel_ingles_id
    ).first()
    if not nivel_ingles:
        raise HTTPException(status_code=404, detail="Nivel de inglés no encontrado")

    db.delete(nivel_ingles)
    db.commit()
    return {"message": "Nivel de inglés eliminado correctamente"}
