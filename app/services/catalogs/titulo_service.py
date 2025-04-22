from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.catalogs.titulo import TituloObtenido
from app.schemas.catalogs.titulo import TituloObtenidoCreate, TituloObtenidoUpdate
from app.utils.orden_catalogos import ordenar_por_nombre

def get_titulo(db: Session, titulo_id: int):
    titulo = db.query(TituloObtenido).filter(TituloObtenido.id_titulo == titulo_id).first()
    if not titulo:
        raise HTTPException(status_code=404, detail="Título no encontrado")
    return titulo

def get_titulos(db: Session, skip: int = 0, limit: int = 100):
    query = db.query(TituloObtenido)
    ordenado = ordenar_por_nombre(query, "nombre_titulo")  # asegúrate que sea el nombre correcto del campo
    return ordenado.offset(skip).limit(limit).all()

def get_titulos_por_nivel(db: Session, id_nivel_educacion: int, skip: int = 0, limit: int = 100):
    query = db.query(TituloObtenido).filter(TituloObtenido.id_nivel_educacion == id_nivel_educacion)
    ordenado = ordenar_por_nombre(query, "nombre_titulo")
    return ordenado.offset(skip).limit(limit).all()



def create_titulo(db: Session, titulo: TituloObtenidoCreate):
    try:
        db_titulo = TituloObtenido(**titulo.model_dump())
        db.add(db_titulo)
        db.commit()
        db.refresh(db_titulo)
        return db_titulo
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el título: {str(e)}")

def update_titulo(db: Session, titulo_id: int, titulo_update: TituloObtenidoUpdate):
    db_titulo = db.query(TituloObtenido).filter(TituloObtenido.id_titulo == titulo_id).first()
    if not db_titulo:
        raise HTTPException(status_code=404, detail="Título no encontrado")
    
    try:
        for key, value in titulo_update.model_dump(exclude_unset=True).items():
            setattr(db_titulo, key, value)
        db.commit()
        db.refresh(db_titulo)
        return db_titulo
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el título: {str(e)}")

def delete_titulo(db: Session, titulo_id: int):
    db_titulo = db.query(TituloObtenido).filter(TituloObtenido.id_titulo == titulo_id).first()
    if not db_titulo:
        raise HTTPException(status_code=404, detail="Título no encontrado")

    try:
        db.delete(db_titulo)
        db.commit()
        return {"message": "Título eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar el título: {str(e)}")
