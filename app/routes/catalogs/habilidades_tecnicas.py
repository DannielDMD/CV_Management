from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.catalogs.habilidades_tecnicas_service import (
    delete_categoria_habilidad, get_categorias_habilidades, get_categoria_habilidad, create_categoria_habilidad,
    get_habilidades_tecnicas, get_habilidad_tecnica, create_habilidad_tecnica, update_categoria_habilidad,
    update_habilidad_tecnica, delete_habilidad_tecnica
)
from app.schemas.habilidades_tecnicas import HabilidadTecnicaCreate, CategoriaHabilidadTecnicaCreate

router = APIRouter(prefix="/habilidades_tecnicas", tags=["Habilidades Técnicas"])

# Obtener todas las categorías de habilidades técnicas
@router.get("/categorias", response_model=list[CategoriaHabilidadTecnicaCreate])
def listar_categorias_habilidades(db: Session = Depends(get_db)):
    return get_categorias_habilidades(db)

# Obtener una categoría específica por ID
@router.get("/categorias/{categoria_id}", response_model=CategoriaHabilidadTecnicaCreate)
def obtener_categoria_habilidad(categoria_id: int, db: Session = Depends(get_db)):
    return get_categoria_habilidad(db, categoria_id)

# Crear una nueva categoría de habilidades técnicas
@router.post("/categorias", response_model=CategoriaHabilidadTecnicaCreate)
def crear_categoria_habilidad(categoria_data: CategoriaHabilidadTecnicaCreate, db: Session = Depends(get_db)):
    return create_categoria_habilidad(db, categoria_data)

@router.put("/categorias/{categoria_id}", response_model=CategoriaHabilidadTecnicaCreate)
def actualizar_categoria_habilidad(categoria_id: int, categoria_data: CategoriaHabilidadTecnicaCreate, db: Session = Depends(get_db)):
    return update_categoria_habilidad(db, categoria_id, categoria_data)


@router.delete("/categorias/{categoria_id}")
def eliminar_categoria_habilidad(categoria_id: int, db: Session = Depends(get_db)):
    return delete_categoria_habilidad(db, categoria_id)




# Obtener todas las habilidades técnicas
@router.get("/", response_model=list[HabilidadTecnicaCreate])
def listar_habilidades_tecnicas(db: Session = Depends(get_db)):
    return get_habilidades_tecnicas(db)

# Obtener una habilidad técnica específica por ID
@router.get("/{habilidad_id}", response_model=HabilidadTecnicaCreate)
def obtener_habilidad_tecnica(habilidad_id: int, db: Session = Depends(get_db)):
    return get_habilidad_tecnica(db, habilidad_id)

# Crear una nueva habilidad técnica (posiblemente con una nueva categoría)
@router.post("/", response_model=HabilidadTecnicaCreate)
def crear_habilidad_tecnica(habilidad_data: HabilidadTecnicaCreate, db: Session = Depends(get_db)):
    return create_habilidad_tecnica(db, habilidad_data)

# Actualizar una habilidad técnica existente
@router.put("/{habilidad_id}", response_model=HabilidadTecnicaCreate)
def actualizar_habilidad_tecnica(habilidad_id: int, habilidad_data: HabilidadTecnicaCreate, db: Session = Depends(get_db)):
    return update_habilidad_tecnica(db, habilidad_id, habilidad_data)

# Eliminar una habilidad técnica
@router.delete("/{habilidad_id}")
def eliminar_habilidad_tecnica(habilidad_id: int, db: Session = Depends(get_db)):
    return delete_habilidad_tecnica(db, habilidad_id)
