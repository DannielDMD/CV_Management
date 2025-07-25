"""
Servicios para la gestión de registros educativos de los candidatos.
Incluye operaciones de creación, consulta, actualización y eliminación.
"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.models.candidato_model import Candidato
from app.models.educacion_model import Educacion
from app.schemas.educacion_schema import EducacionCreate, EducacionUpdate


def create_educacion(db: Session, educacion_data: EducacionCreate) -> Educacion:
    """
    Registra un nuevo antecedente educativo para un candidato.

    Args:
        db (Session): Sesión activa de la base de datos.
        educacion_data (EducacionCreate): Datos del registro educativo a insertar.

    Returns:
        Educacion: Objeto de educación creado.

    Raises:
        HTTPException:
            - 404 si el candidato no existe.
            - 400 si el año de graduación es anterior al año de nacimiento del candidato.
            - 500 si ocurre un error al guardar en la base de datos.
    """
    candidato = db.query(Candidato).filter(Candidato.id_candidato == educacion_data.id_candidato).first()
    if not candidato:
        raise HTTPException(status_code=404, detail="Candidato no encontrado.")

    if educacion_data.anio_graduacion and candidato.fecha_nacimiento:
        año_nacimiento = candidato.fecha_nacimiento.year
        if educacion_data.anio_graduacion < año_nacimiento:
            raise HTTPException(
                status_code=400,
                detail=f"El año de graduación ({educacion_data.anio_graduacion}) no puede ser anterior al año de nacimiento ({año_nacimiento})."
            )

    nueva_educacion = Educacion(**educacion_data.model_dump())
    try:
        db.add(nueva_educacion)
        db.commit()
        db.refresh(nueva_educacion)
        return nueva_educacion
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Error al insertar la educación en la base de datos"
        )


def get_educacion_by_id(db: Session, id_educacion: int) -> Educacion:
    """
    Recupera un registro de educación a partir de su ID.

    Args:
        db (Session): Sesión activa de la base de datos.
        id_educacion (int): ID del registro educativo.

    Returns:
        Educacion: Objeto de educación encontrado.

    Raises:
        HTTPException: 404 si no se encuentra el registro.
    """
    educacion = db.query(Educacion).filter(Educacion.id_educacion == id_educacion).first()
    if not educacion:
        raise HTTPException(status_code=404, detail="Educación no encontrada")
    return educacion


def get_all_educaciones(db: Session) -> list[Educacion]:
    """
    Devuelve todos los registros educativos existentes en el sistema.

    Args:
        db (Session): Sesión activa de la base de datos.

    Returns:
        list[Educacion]: Lista completa de registros educativos.
    """
    return db.query(Educacion).all()


def get_educaciones_by_candidato(db: Session, id_candidato: int) -> list[Educacion]:
    """
    Obtiene todas las educaciones asociadas a un candidato específico.

    Args:
        db (Session): Sesión activa de la base de datos.
        id_candidato (int): ID del candidato.

    Returns:
        list[Educacion]: Lista de registros educativos del candidato.

    Raises:
        HTTPException: 404 si no se encuentran registros asociados.
    """
    educaciones = db.query(Educacion).filter(Educacion.id_candidato == id_candidato).all()
    if not educaciones:
        raise HTTPException(status_code=404, detail="No se encontraron educaciones para este candidato")
    return educaciones


def update_educacion(db: Session, id_educacion: int, educacion_data: EducacionUpdate) -> Educacion:
    """
    Actualiza un registro educativo existente por su ID.

    Args:
        db (Session): Sesión activa de la base de datos.
        id_educacion (int): ID del registro a modificar.
        educacion_data (EducacionUpdate): Nuevos datos a actualizar.

    Returns:
        Educacion: Registro actualizado.

    Raises:
        HTTPException: 404 si el registro no existe.
    """
    educacion = db.query(Educacion).filter(Educacion.id_educacion == id_educacion).first()
    if not educacion:
        raise HTTPException(status_code=404, detail="Educación no encontrada")

    for key, value in educacion_data.model_dump(exclude_unset=True).items():
        setattr(educacion, key, value)

    db.commit()
    db.refresh(educacion)
    return educacion


def delete_educacion(db: Session, id_educacion: int) -> dict:
    """
    Elimina un registro educativo por su ID.

    Args:
        db (Session): Sesión activa de la base de datos.
        id_educacion (int): ID del registro a eliminar.

    Returns:
        dict: Mensaje de confirmación de eliminación.

    Raises:
        HTTPException: 404 si el registro no existe.
    """
    educacion = db.query(Educacion).filter(Educacion.id_educacion == id_educacion).first()
    if not educacion:
        raise HTTPException(status_code=404, detail="Educación no encontrada")

    db.delete(educacion)
    db.commit()
    return {"message": "Educación eliminada correctamente"}
