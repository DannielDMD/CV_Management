from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.catalogs.categorias_cargos_service import (
    obtener_categorias_cargo,
    obtener_categoria_cargo_por_id,
    crear_categoria_cargo,
    actualizar_categoria_cargo,
    eliminar_categoria_cargo
)
from app.schemas.catalogs.categoria_cargo import CategoriaCargoCreate, CategoriaCargoResponse

router = APIRouter(
    prefix="/categorias-cargo",
    tags=["Categorías de Cargo"]
)

# Obtener todas las categorías de cargo
@router.get("/", response_model=list[CategoriaCargoResponse])
def get_categorias_cargo(db: Session = Depends(get_db)):
    return obtener_categorias_cargo(db)

# Obtener una categoría de cargo por ID
@router.get("/{id_categoria}", response_model=CategoriaCargoResponse)
def get_categoria_cargo(id_categoria: int, db: Session = Depends(get_db)):
    return obtener_categoria_cargo_por_id(db, id_categoria)

# Crear una nueva categoría de cargo
@router.post("/", response_model=CategoriaCargoResponse)
def post_categoria_cargo(categoria_data: CategoriaCargoCreate, db: Session = Depends(get_db)):
    return crear_categoria_cargo(db, categoria_data)

# Actualizar una categoría de cargo
@router.put("/{id_categoria}", response_model=CategoriaCargoResponse)
def put_categoria_cargo(id_categoria: int, categoria_data: CategoriaCargoCreate, db: Session = Depends(get_db)):
    return actualizar_categoria_cargo(db, id_categoria, categoria_data)

# Eliminar una categoría de cargo
@router.delete("/{id_categoria}")
def delete_categoria_cargo(id_categoria: int, db: Session = Depends(get_db)):
    return eliminar_categoria_cargo(db, id_categoria)
