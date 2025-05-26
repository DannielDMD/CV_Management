"""
Servicios para gestionar el catálogo de Motivos de Salida.
Incluye funciones para listar, obtener, crear, actualizar y eliminar motivos.
"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

from app.models.preferencias import MotivoSalida
from app.schemas.catalogs.motivo_salida import MotivoSalidaCreate, MotivoSalidaUpdate
from app.utils.orden_catalogos import ordenar_por_nombre


def get_motivos_salida(db: Session):
    """
    Retorna todos los motivos de salida ordenados alfabéticamente.

    Args:
        db (Session): Sesión de base de datos.

    Returns:
        List[MotivoSalida]: Lista de motivos ordenados.

    Raises:
        HTTPException: Si ocurre un error de base de datos.
    """
    try:
        query = db.query(MotivoSalida)
        ordenado = ordenar_por_nombre(query, "descripcion_motivo")
        return ordenado.all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener motivos de salida: {str(e)}")


def get_motivo_salida(db: Session, motivo_id: int):
    """
    Obtiene un motivo de salida por su ID.

    Args:
        db (Session): Sesión de base de datos.
        motivo_id (int): ID del motivo.

    Returns:
        MotivoSalida: Objeto encontrado.

    Raises:
        HTTPException: Si no se encuentra o falla la consulta.
    """
    try:
        motivo = db.query(MotivoSalida).filter(MotivoSalida.id_motivo_salida == motivo_id).first()
        if not motivo:
            raise HTTPException(status_code=404, detail="Motivo de salida no encontrado")
        return motivo
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el motivo de salida: {str(e)}")


def create_motivo_salida(db: Session, motivo_data: MotivoSalidaCreate):
    """
    Crea un nuevo motivo de salida.

    Args:
        db (Session): Sesión de base de datos.
        motivo_data (MotivoSalidaCreate): Datos del motivo.

    Returns:
        MotivoSalida: Objeto creado.

    Raises:
        HTTPException: Si ocurre un error al guardar.
    """
    try:
        nuevo_motivo = MotivoSalida(**motivo_data.dict())
        db.add(nuevo_motivo)
        db.commit()
        db.refresh(nuevo_motivo)
        return nuevo_motivo
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear motivo de salida: {str(e)}")


def update_motivo_salida(db: Session, motivo_id: int, motivo_data: MotivoSalidaUpdate):
    """
    Actualiza un motivo de salida existente.

    Args:
        db (Session): Sesión de base de datos.
        motivo_id (int): ID del motivo a actualizar.
        motivo_data (MotivoSalidaUpdate): Campos a modificar.

    Returns:
        MotivoSalida: Motivo actualizado.

    Raises:
        HTTPException: Si no se encuentra o falla la actualización.
    """
    try:
        motivo = db.query(MotivoSalida).filter(MotivoSalida.id_motivo_salida == motivo_id).first()
        if not motivo:
            raise HTTPException(status_code=404, detail="Motivo de salida no encontrado")
        
        for key, value in motivo_data.dict(exclude_unset=True).items():
            setattr(motivo, key, value)
        
        db.commit()
        db.refresh(motivo)
        return motivo
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar motivo de salida: {str(e)}")


def delete_motivo_salida(db: Session, motivo_id: int):
    """
    Elimina un motivo de salida por su ID.

    Args:
        db (Session): Sesión de base de datos.
        motivo_id (int): ID del motivo a eliminar.

    Returns:
        dict: Mensaje de éxito.

    Raises:
        HTTPException: Si no se encuentra o falla la eliminación.
    """
    try:
        motivo = db.query(MotivoSalida).filter(MotivoSalida.id_motivo_salida == motivo_id).first()
        if not motivo:
            raise HTTPException(status_code=404, detail="Motivo de salida no encontrado")
        
        db.delete(motivo)
        db.commit()
        return {"message": "Motivo de salida eliminado exitosamente"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar motivo de salida: {str(e)}")
