"""
Servicios para la gestión de cargos ofrecidos.
Incluye operaciones CRUD básicas y validaciones.
"""

import math
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.catalogs.cargo_ofrecido import CargoOfrecido
from app.schemas.catalogs.cargo_ofrecido import CargoOfrecidoCreate, CargoOfrecidoPaginatedResponse
from app.utils.orden_catalogos import ordenar_por_nombre


def obtener_cargos_ofrecidos(db: Session):
    query = db.query(CargoOfrecido)
    return ordenar_por_nombre(query, "nombre_cargo").all()


def obtener_cargo_ofrecido_por_id(db: Session, id_cargo: int):
    """
    Obtiene un cargo ofrecido por su ID.

    Args:
        db (Session): Sesión de base de datos.
        id_cargo (int): ID del cargo.

    Returns:
        CargoOfrecido: Objeto cargo si existe.

    Raises:
        HTTPException: Si el cargo no existe.
    """
    cargo = db.query(CargoOfrecido).filter(CargoOfrecido.id_cargo == id_cargo).first()
    if not cargo:
        raise HTTPException(status_code=404, detail="Cargo no encontrado")
    return cargo


def obtener_cargos_por_categoria(db: Session, id_categoria: int):
    """
    Obtiene los cargos asociados a una categoría específica.

    Args:
        db (Session): Sesión de base de datos.
        id_categoria (int): ID de la categoría.

    Returns:
        List[CargoOfrecido]: Lista de cargos encontrados.

    Raises:
        HTTPException: Si no hay cargos en esa categoría.
    """
    cargos = db.query(CargoOfrecido).filter(CargoOfrecido.id_categoria == id_categoria).all()
    if not cargos:
        raise HTTPException(status_code=404, detail="No hay cargos en esta categoría")
    return cargos

"""
Servicio para el tema de paginación y búqueda
"""
def get_cargos_con_paginacion(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None
) -> CargoOfrecidoPaginatedResponse:
    """
    Retorna cargos ofrecidos con búsqueda y paginación.
    """
    query = db.query(CargoOfrecido)

    if search:
        query = query.filter(CargoOfrecido.nombre_cargo.ilike(f"%{search}%"))

    total = query.count()

    resultados = query.order_by(CargoOfrecido.nombre_cargo.asc())\
        .offset(skip).limit(limit).all()

    page = (skip // limit) + 1 if limit > 0 else 1
    total_pages = math.ceil(total / limit) if limit > 0 else 1

    return CargoOfrecidoPaginatedResponse(
        total=total,
        page=page,
        per_page=limit,
        total_pages=total_pages,
        resultados=resultados
    )



def crear_cargo_ofrecido(db: Session, cargo_data: CargoOfrecidoCreate):
    """
    Crea un nuevo cargo ofrecido, verificando duplicados por nombre.

    Args:
        db (Session): Sesión de base de datos.
        cargo_data (CargoOfrecidoCreate): Datos del nuevo cargo.

    Returns:
        CargoOfrecido: Cargo creado exitosamente.

    Raises:
        HTTPException: Si el nombre del cargo ya existe.
    """
    existing_cargo = db.query(CargoOfrecido).filter(
        CargoOfrecido.nombre_cargo == cargo_data.nombre_cargo
    ).first()

    if existing_cargo:
        raise HTTPException(status_code=400, detail="El cargo ya existe")

    nuevo_cargo = CargoOfrecido(nombre_cargo=cargo_data.nombre_cargo)
    db.add(nuevo_cargo)
    db.commit()
    db.refresh(nuevo_cargo)
    return nuevo_cargo

def actualizar_cargo_ofrecido(db: Session, id_cargo: int, cargo_data: CargoOfrecidoCreate):
    """
    Actualiza un cargo ofrecido existente.

    Args:
        db (Session): Sesión de base de datos.
        id_cargo (int): ID del cargo a actualizar.
        cargo_data (CargoOfrecidoCreate): Nuevos datos del cargo.

    Returns:
        CargoOfrecido: Cargo actualizado.

    Raises:
        HTTPException: Si el cargo no existe o el nuevo nombre ya está en uso por otro.
    """
    cargo = db.query(CargoOfrecido).filter(CargoOfrecido.id_cargo == id_cargo).first()
    if not cargo:
        raise HTTPException(status_code=404, detail="Cargo no encontrado")

    # Verificar que no exista otro con ese nombre
    existe = db.query(CargoOfrecido).filter(
        CargoOfrecido.nombre_cargo == cargo_data.nombre_cargo,
        CargoOfrecido.id_cargo != id_cargo
    ).first()
    if existe:
        raise HTTPException(status_code=400, detail="Ya existe un cargo con ese nombre")

    cargo.nombre_cargo = cargo_data.nombre_cargo
    db.commit()
    db.refresh(cargo)
    return cargo


def eliminar_cargo_ofrecido(db: Session, id_cargo: int):
    """
    Elimina un cargo ofrecido por su ID.

    Args:
        db (Session): Sesión de base de datos.
        id_cargo (int): ID del cargo a eliminar.

    Returns:
        dict: Mensaje de confirmación.

    Raises:
        HTTPException: Si el cargo no existe.
    """
    cargo = db.query(CargoOfrecido).filter(CargoOfrecido.id_cargo == id_cargo).first()
    if not cargo:
        raise HTTPException(status_code=404, detail="Cargo no encontrado")

    db.delete(cargo)
    db.commit()
    return {"detail": "Cargo eliminado correctamente"}
