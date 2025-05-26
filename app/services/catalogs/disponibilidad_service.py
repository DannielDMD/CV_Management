"""
Servicios para el catálogo de Disponibilidad.
Incluye operaciones CRUD con validaciones de duplicidad y existencia.
"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, NoResultFound
from app.models.preferencias import Disponibilidad
from app.schemas.preferencias_schema import DisponibilidadCreate, DisponibilidadUpdate


def get_all_disponibilidades(db: Session):
    """
    Retorna todas las disponibilidades registradas.

    Args:
        db (Session): Sesión activa de la base de datos.

    Returns:
        List[Disponibilidad]: Lista de registros de disponibilidad.
    """
    return db.query(Disponibilidad).all()


def get_disponibilidad(db: Session, disponibilidad_id: int):
    """
    Obtiene una disponibilidad por su ID.

    Args:
        db (Session): Sesión activa.
        disponibilidad_id (int): ID a buscar.

    Returns:
        Disponibilidad: Objeto disponibilidad encontrado.

    Raises:
        NoResultFound: Si el ID no existe en la base de datos.
    """
    disponibilidad = (
        db.query(Disponibilidad)
        .filter(Disponibilidad.id_disponibilidad == disponibilidad_id)
        .first()
    )
    if not disponibilidad:
        raise NoResultFound(f"Disponibilidad con ID {disponibilidad_id} no encontrada")
    return disponibilidad


def create_disponibilidad(db: Session, disponibilidad_data: DisponibilidadCreate):
    """
    Crea una nueva disponibilidad si no existe una igual.

    Args:
        db (Session): Sesión activa.
        disponibilidad_data (DisponibilidadCreate): Datos a registrar.

    Returns:
        Disponibilidad: Registro creado.

    Raises:
        ValueError: Si ya existe una disponibilidad con el mismo nombre.
    """
    try:
        nueva_disponibilidad = Disponibilidad(
            descripcion_disponibilidad=disponibilidad_data.descripcion_disponibilidad
        )
        db.add(nueva_disponibilidad)
        db.commit()
        db.refresh(nueva_disponibilidad)
        return nueva_disponibilidad
    except IntegrityError:
        db.rollback()
        raise ValueError("Ya existe una Disponibilidad con esa descripción")


def update_disponibilidad(db: Session, disponibilidad_id: int, disponibilidad_data: DisponibilidadUpdate):
    """
    Actualiza una disponibilidad por su ID.

    Args:
        db (Session): Sesión activa.
        disponibilidad_id (int): ID del registro a modificar.
        disponibilidad_data (DisponibilidadUpdate): Nuevos datos.

    Returns:
        Disponibilidad: Objeto actualizado.
    """
    disponibilidad = get_disponibilidad(db, disponibilidad_id)
    if disponibilidad_data.descripcion_disponibilidad:
        disponibilidad.descripcion_disponibilidad = disponibilidad_data.descripcion_disponibilidad
    db.commit()
    db.refresh(disponibilidad)
    return disponibilidad


def delete_disponibilidad(db: Session, disponibilidad_id: int):
    """
    Elimina una disponibilidad por su ID.

    Args:
        db (Session): Sesión activa.
        disponibilidad_id (int): ID a eliminar.

    Returns:
        dict: Mensaje de confirmación.
    """
    disponibilidad = get_disponibilidad(db, disponibilidad_id)
    db.delete(disponibilidad)
    db.commit()
    return {
        "message": f"Disponibilidad con ID {disponibilidad_id} eliminada correctamente"
    }
