"""Servicios para la gestión de departamentos."""

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models.catalogs.ciudad import Departamento
from app.schemas.catalogs.ciudad import (
    DepartamentoCreate,
)

from typing import List, Optional



def crear_departamento(db: Session, departamento_data: DepartamentoCreate) -> Optional[Departamento]:
    nombre = departamento_data.nombre_departamento.strip()
    existente = db.query(Departamento).filter(Departamento.nombre_departamento.ilike(nombre)).first()
    if existente:
        return None  # Ya existe, no se debe duplicar

    nuevo_departamento = Departamento(nombre_departamento=nombre)
    db.add(nuevo_departamento)
    try:
        db.commit()
        db.refresh(nuevo_departamento)
        return nuevo_departamento
    except IntegrityError:
        db.rollback()
        return None


def obtener_todos_departamentos(db: Session) -> List[Departamento]:
    return db.query(Departamento).order_by(Departamento.nombre_departamento.asc()).all()


def obtener_departamento_por_id(db: Session, id_departamento: int) -> Optional[Departamento]:
    return db.query(Departamento).filter(Departamento.id_departamento == id_departamento).first()


def actualizar_departamento(db: Session, id_departamento: int, datos_update: DepartamentoCreate) -> Optional[Departamento]:
    departamento = obtener_departamento_por_id(db, id_departamento)
    if not departamento:
        return None

    nuevo_nombre = datos_update.nombre_departamento.strip()
    existe_otro = db.query(Departamento).filter(
        Departamento.nombre_departamento.ilike(nuevo_nombre),
        Departamento.id_departamento != id_departamento
    ).first()

    if existe_otro:
        return None  # Conflicto por nombre duplicado

    departamento.nombre_departamento = nuevo_nombre
    try:
        db.commit()
        db.refresh(departamento)
        return departamento
    except IntegrityError:
        db.rollback()
        return None


def eliminar_departamento(db: Session, id_departamento: int) -> bool:
    departamento = obtener_departamento_por_id(db, id_departamento)
    if not departamento:
        return False
    try:
        db.delete(departamento)
        db.commit()
        return True
    except IntegrityError:
        db.rollback()
        return False
