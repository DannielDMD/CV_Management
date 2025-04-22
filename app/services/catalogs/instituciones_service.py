from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.catalogs.instituciones import InstitucionAcademica
from app.schemas.catalogs.instituciones import (
    InstitucionAcademicaCreate,
    InstitucionAcademicaUpdate,
)
from app.utils.orden_catalogos import ordenar_por_nombre


def get_institucion(db: Session, institucion_id: int):
    institucion = (
        db.query(InstitucionAcademica)
        .filter(InstitucionAcademica.id_institucion == institucion_id)
        .first()
    )
    if not institucion:
        raise HTTPException(status_code=404, detail="Institución no encontrada")
    return institucion


def get_instituciones(db: Session, skip: int = 0, limit: int = 100):
    query = db.query(InstitucionAcademica)
    ordenado = ordenar_por_nombre(
        query, "nombre_institucion"
    )  # campo exacto del modelo
    return ordenado.offset(skip).limit(limit).all()


def create_institucion(db: Session, institucion: InstitucionAcademicaCreate):
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


def update_institucion(
    db: Session, institucion_id: int, institucion_update: InstitucionAcademicaUpdate
):
    db_institucion = (
        db.query(InstitucionAcademica)
        .filter(InstitucionAcademica.id_institucion == institucion_id)
        .first()
    )
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
    db_institucion = (
        db.query(InstitucionAcademica)
        .filter(InstitucionAcademica.id_institucion == institucion_id)
        .first()
    )
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
