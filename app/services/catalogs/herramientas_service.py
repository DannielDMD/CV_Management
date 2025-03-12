from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.herramientas import CategoriaHerramienta, Herramienta
from app.schemas.herramientas import CategoriaHerramientaCreate, CategoriaHerramientaUpdate, HerramientaCreate, HerramientaUpdate

def create_categoria_herramienta(db: Session, categoria_data: CategoriaHerramientaCreate):
    existing_categoria = db.query(CategoriaHerramienta).filter_by(nombre_categoria=categoria_data.nombre_categoria).first()
    if existing_categoria:
        raise HTTPException(status_code=400, detail="La categoría de herramienta ya existe.")
    
    new_categoria = CategoriaHerramienta(**categoria_data.model_dump())
    db.add(new_categoria)
    db.commit()
    db.refresh(new_categoria)
    return new_categoria

def get_categoria_herramienta(db: Session, categoria_id: int):
    categoria = db.query(CategoriaHerramienta).filter_by(id_categoria_herramienta=categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría de herramienta no encontrada.")
    return categoria

def get_categorias_herramientas(db: Session):
    return db.query(CategoriaHerramienta).all()

def update_categoria_herramienta(db: Session, categoria_id: int, categoria_data: CategoriaHerramientaUpdate):
    categoria = db.query(CategoriaHerramienta).filter_by(id_categoria_herramienta=categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría de herramienta no encontrada.")
    
    categoria.nombre_categoria = categoria_data.nombre_categoria
    db.commit()
    db.refresh(categoria)
    return categoria

def delete_categoria_herramienta(db: Session, categoria_id: int):
    categoria = db.query(CategoriaHerramienta).filter_by(id_categoria_herramienta=categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría de herramienta no encontrada.")
    
    if categoria.herramientas:
        raise HTTPException(status_code=400, detail="No se puede eliminar una categoría con herramientas asociadas.")
    
    db.delete(categoria)
    db.commit()
    return {"message": "Categoría eliminada exitosamente."}

def create_herramienta(db: Session, herramienta_data: HerramientaCreate):
    categoria = db.query(CategoriaHerramienta).filter_by(id_categoria_herramienta=herramienta_data.id_categoria_herramienta).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="La categoría de herramienta no existe.")
    
    existing_herramienta = db.query(Herramienta).filter_by(nombre_herramienta=herramienta_data.nombre_herramienta).first()
    if existing_herramienta:
        raise HTTPException(status_code=400, detail="La herramienta ya existe.")
    
    new_herramienta = Herramienta(**herramienta_data.model_dump())
    db.add(new_herramienta)
    db.commit()
    db.refresh(new_herramienta)
    return new_herramienta

def get_herramienta(db: Session, herramienta_id: int):
    herramienta = db.query(Herramienta).filter_by(id_herramienta=herramienta_id).first()
    if not herramienta:
        raise HTTPException(status_code=404, detail="Herramienta no encontrada.")
    return herramienta

def get_herramientas(db: Session):
    return db.query(Herramienta).all()

def update_herramienta(db: Session, herramienta_id: int, herramienta_data: HerramientaUpdate):
    herramienta = db.query(Herramienta).filter_by(id_herramienta=herramienta_id).first()
    if not herramienta:
        raise HTTPException(status_code=404, detail="Herramienta no encontrada.")
    
    if herramienta_data.id_categoria_herramienta:
        categoria = db.query(CategoriaHerramienta).filter_by(id_categoria_herramienta=herramienta_data.id_categoria_herramienta).first()
        if not categoria:
            raise HTTPException(status_code=404, detail="La categoría de herramienta no existe.")
    
    herramienta.nombre_herramienta = herramienta_data.nombre_herramienta
    herramienta.id_categoria_herramienta = herramienta_data.id_categoria_herramienta
    db.commit()
    db.refresh(herramienta)
    return herramienta

def delete_herramienta(db: Session, herramienta_id: int):
    herramienta = db.query(Herramienta).filter_by(id_herramienta=herramienta_id).first()
    if not herramienta:
        raise HTTPException(status_code=404, detail="Herramienta no encontrada.")
    
    db.delete(herramienta)
    db.commit()
    return {"message": "Herramienta eliminada exitosamente."}