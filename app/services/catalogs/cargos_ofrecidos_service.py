"""
Servicios para la gestión de cargos ofrecidos.
Incluye operaciones CRUD básicas y validaciones.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.catalogs.cargo_ofrecido import CargoOfrecido
from app.schemas.catalogs.cargo_ofrecido import CargoOfrecidoCreate
from app.utils.orden_catalogos import ordenar_por_nombre


def obtener_cargos_ofrecidos(db: Session):
    """
    Obtiene todos los cargos ofrecidos ordenados alfabéticamente por nombre.

    Args:
        db (Session): Sesión de base de datos.

    Returns:
        List[CargoOfrecido]: Lista de cargos ordenados.
    """
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
