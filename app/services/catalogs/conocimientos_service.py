from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.models.conocimientos_model import HabilidadBlanda, HabilidadTecnica, Herramienta
from app.schemas.catalogs.conocimientos_schema import HabilidadBlandaResponse, HabilidadTecnicaResponse, HerramientaResponse
from app.utils.orden_catalogos import ordenar_por_nombre

def get_habilidades_blandas(db: Session):
    try:
        query = db.query(HabilidadBlanda)
        ordenado = ordenar_por_nombre(query, "nombre_habilidad_blanda").all()
        if not ordenado:
            raise HTTPException(status_code=404, detail="No se encontraron habilidades blandas")
        return [HabilidadBlandaResponse.model_validate(h) for h in ordenado]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener habilidades blandas: {str(e)}")

def get_habilidades_tecnicas(db: Session):
    try:
        query = db.query(HabilidadTecnica)
        ordenado = ordenar_por_nombre(query, "nombre_habilidad_tecnica").all()
        if not ordenado:
            raise HTTPException(status_code=404, detail="No se encontraron habilidades técnicas")
        return [HabilidadTecnicaResponse.model_validate(h) for h in ordenado]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener habilidades técnicas: {str(e)}")

def get_herramientas(db: Session):
    try:
        query = db.query(Herramienta)
        ordenado = ordenar_por_nombre(query, "nombre_herramienta").all()
        if not ordenado:
            raise HTTPException(status_code=404, detail="No se encontraron herramientas")
        return [HerramientaResponse.model_validate(h) for h in ordenado]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener herramientas: {str(e)}")
