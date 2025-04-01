from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.models.conocimientos_model import HabilidadBlanda, HabilidadTecnica, Herramienta
from app.schemas.catalogs.conocimientos_schema import HabilidadBlandaResponse, HabilidadTecnicaResponse, HerramientaResponse

def get_habilidades_blandas(db: Session):
    try:
        habilidades = db.query(HabilidadBlanda).all()
        if not habilidades:
            raise HTTPException(status_code=404, detail="No se encontraron habilidades blandas")
        return [HabilidadBlandaResponse.model_validate(habilidad) for habilidad in habilidades]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener habilidades blandas: {str(e)}")

def get_habilidades_tecnicas(db: Session):
    try:
        habilidades = db.query(HabilidadTecnica).all()
        if not habilidades:
            raise HTTPException(status_code=404, detail="No se encontraron habilidades técnicas")
        return [HabilidadTecnicaResponse.model_validate(habilidad) for habilidad in habilidades]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener habilidades técnicas: {str(e)}")

def get_herramientas(db: Session):
    try:
        herramientas = db.query(Herramienta).all()
        if not herramientas:
            raise HTTPException(status_code=404, detail="No se encontraron herramientas")
        return [HerramientaResponse.model_validate(herramienta) for herramienta in herramientas]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener herramientas: {str(e)}")
