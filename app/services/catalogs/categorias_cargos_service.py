"""from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.catalogs.categoria_cargo import CategoriaCargo
from app.schemas.catalogs.categoria_cargo import CategoriaCargoCreate, CategoriaCargoResponse


# Obtener todas las categorías de cargo
def obtener_categorias_cargo(db: Session):
    return db.query(CategoriaCargo).all()

# Obtener una categoría de cargo por ID
def obtener_categoria_cargo_por_id(db: Session, id_categoria: int):
    categoria = db.query(CategoriaCargo).filter(CategoriaCargo.id_categoria == id_categoria).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria

# Crear una nueva categoría de cargo
def crear_categoria_cargo(db: Session, categoria_data: CategoriaCargoCreate):
    # Verificar si la categoría ya existe
    existing_categoria = db.query(CategoriaCargo).filter(CategoriaCargo.nombre_categoria == categoria_data.nombre_categoria).first()
    if existing_categoria:
        raise HTTPException(status_code=400, detail="La categoría ya existe")

    nueva_categoria = CategoriaCargo(nombre_categoria=categoria_data.nombre_categoria)
    db.add(nueva_categoria)
    db.commit()
    db.refresh(nueva_categoria)
    return nueva_categoria

# Actualizar una categoría de cargo
def actualizar_categoria_cargo(db: Session, id_categoria: int, categoria_data: CategoriaCargoCreate):
    categoria = db.query(CategoriaCargo).filter(CategoriaCargo.id_categoria == id_categoria).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    for key, value in categoria_data.model_dump().items():
        setattr(categoria, key, value)

    db.commit()
    db.refresh(categoria)
    return categoria

# Eliminar una categoría de cargo
def eliminar_categoria_cargo(db: Session, id_categoria: int):
    categoria = db.query(CategoriaCargo).filter(CategoriaCargo.id_categoria == id_categoria).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    db.delete(categoria)
    db.commit()
    return {"detail": "Categoría eliminada correctamente"}
"""