from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.catalogs.cargo_ofrecido import CargoOfrecido
from app.schemas.catalogs.cargo_ofrecido import CargoOfrecidoCreate

def obtener_cargos_ofrecidos(db: Session):
    return db.query(CargoOfrecido).all()

def obtener_cargo_ofrecido_por_id(db: Session, id_cargo: int):
    cargo = db.query(CargoOfrecido).filter(CargoOfrecido.id_cargo == id_cargo).first()
    if not cargo:
        raise HTTPException(status_code=404, detail="Cargo no encontrado")
    return cargo

def obtener_cargos_por_categoria(db: Session, id_categoria: int):
    cargos = db.query(CargoOfrecido).filter(CargoOfrecido.id_categoria == id_categoria).all()
    if not cargos:
        raise HTTPException(status_code=404, detail="No hay cargos en esta categoría")
    return cargos

def crear_cargo_ofrecido(db: Session, cargo_data: CargoOfrecidoCreate):
    # Verificar si ya existe un cargo con el mismo nombre
    existing_cargo = db.query(CargoOfrecido).filter(CargoOfrecido.nombre_cargo == cargo_data.nombre_cargo).first()
    if existing_cargo:
        raise HTTPException(status_code=400, detail="El cargo ya existe")
    
    nuevo_cargo = CargoOfrecido(nombre_cargo=cargo_data.nombre_cargo)
    db.add(nuevo_cargo)
    db.commit()
    db.refresh(nuevo_cargo)
    return nuevo_cargo

def eliminar_cargo_ofrecido(db: Session, id_cargo: int):
    cargo = db.query(CargoOfrecido).filter(CargoOfrecido.id_cargo == id_cargo).first()
    if not cargo:
        raise HTTPException(status_code=404, detail="Cargo no encontrado")
    
    db.delete(cargo)
    db.commit()
    return {"detail": "Cargo eliminado correctamente"}
