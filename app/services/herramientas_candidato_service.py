from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.herramientas import CategoriaHerramienta, Herramienta, HerramientaCandidato
from app.schemas.herramientas import CategoriaHerramientaResponse, HerramientaResponse, HerramientaCandidatoCreate, HerramientaCandidatoResponse

def obtener_categorias_herramientas(db: Session):
    categorias = db.query(CategoriaHerramienta).all()
    if not categorias:
        raise HTTPException(status_code=404, detail="No se encontraron categorías de herramientas")
    return categorias

def obtener_herramientas_por_categoria(db: Session, id_categoria: int):
    herramientas = db.query(Herramienta).filter(Herramienta.id_categoria_herramienta == id_categoria).all()
    if not herramientas:
        raise HTTPException(status_code=404, detail=f"No se encontraron herramientas para la categoría {id_categoria}")
    return herramientas

def obtener_herramientas_candidato(db: Session, id_candidato: int):
    herramientas_candidato = db.query(HerramientaCandidato).filter(HerramientaCandidato.id_candidato == id_candidato).all()
    if not herramientas_candidato:
        raise HTTPException(status_code=404, detail=f"No se encontraron herramientas asignadas al candidato {id_candidato}")
    return [HerramientaCandidatoResponse(id=h.id, herramienta=h.herramienta) for h in herramientas_candidato]

def asignar_herramienta_a_candidato(db: Session, herramienta_data: HerramientaCandidatoCreate):
    herramienta_existente = db.query(HerramientaCandidato).filter(
        HerramientaCandidato.id_candidato == herramienta_data.id_candidato,
        HerramientaCandidato.id_herramienta == herramienta_data.id_herramienta
    ).first()
    if herramienta_existente:
        raise HTTPException(status_code=400, detail="El candidato ya tiene asignada esta herramienta")
    
    nueva_herramienta_candidato = HerramientaCandidato(**herramienta_data.model_dump())
    try:
        db.add(nueva_herramienta_candidato)
        db.commit()
        db.refresh(nueva_herramienta_candidato)
        return nueva_herramienta_candidato
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al asignar la herramienta al candidato")

def eliminar_herramienta_de_candidato(db: Session, id_candidato: int, id_herramienta: int):
    herramienta_candidato = db.query(HerramientaCandidato).filter(
        HerramientaCandidato.id_candidato == id_candidato,
        HerramientaCandidato.id_herramienta == id_herramienta
    ).first()
    
    if not herramienta_candidato:
        raise HTTPException(status_code=404, detail="Herramienta no encontrada para el candidato")
    
    try:
        db.delete(herramienta_candidato)
        db.commit()
        return {"message": "Herramienta eliminada correctamente"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al eliminar la herramienta del candidato")
