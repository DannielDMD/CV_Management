from typing import List
from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.conocimientos_candidato_schema import CandidatoConocimientoCreate, CandidatoConocimientoResponse
from app.services.conocimientos_candidato_service import (
    get_conocimiento,
    create_conocimiento,
    delete_conocimiento
)
from app.core.database import get_db

router = APIRouter(
    prefix="/conocimientos-candidato",
    tags=["Conocimientos Candidato"]
)



@router.post("/", status_code=201)
def create_conocimientos_endpoint(
    conocimientos: List[CandidatoConocimientoCreate],
    db: Session = Depends(get_db)
):
    creados = []
    for conocimiento in conocimientos:
        nuevo = create_conocimiento(db, conocimiento)
        creados.append(nuevo)
    return JSONResponse(content={"detalles": f"{len(creados)} conocimientos creados con éxito"})




@router.get("/{conocimiento_id}", response_model=CandidatoConocimientoResponse)
def get_conocimiento_endpoint(conocimiento_id: int, db: Session = Depends(get_db)):
    return get_conocimiento(db, conocimiento_id)

@router.delete("/{conocimiento_id}", status_code=204)
def delete_conocimiento_endpoint(conocimiento_id: int, db: Session = Depends(get_db)):
    delete_conocimiento(db, conocimiento_id)
    return None  # HTTP 204 No Content
