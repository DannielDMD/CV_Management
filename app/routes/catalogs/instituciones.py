from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.catalogs.instituciones import InstitucionAcademicaCreate, InstitucionAcademicaUpdate, InstitucionAcademicaResponse
from app.services.catalogs.instituciones_service import get_institucion, get_instituciones, create_institucion, update_institucion, delete_institucion

router = APIRouter(prefix="/instituciones", tags=["Instituciones Académicas"])

@router.get("/", response_model=list[InstitucionAcademicaResponse])
def read_instituciones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_instituciones(db, skip, limit)

@router.get("/{institucion_id}", response_model=InstitucionAcademicaResponse)
def read_institucion(institucion_id: int, db: Session = Depends(get_db)):
    return get_institucion(db, institucion_id)

@router.post("/", response_model=InstitucionAcademicaResponse, status_code=201)
def create_institucion_endpoint(institucion: InstitucionAcademicaCreate, db: Session = Depends(get_db)):
    return create_institucion(db, institucion)

@router.put("/{institucion_id}", response_model=InstitucionAcademicaResponse)
def update_institucion_endpoint(institucion_id: int, institucion_update: InstitucionAcademicaUpdate, db: Session = Depends(get_db)):
    return update_institucion(db, institucion_id, institucion_update)

@router.delete("/{institucion_id}")
def delete_institucion_endpoint(institucion_id: int, db: Session = Depends(get_db)):
    return delete_institucion(db, institucion_id)
