from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.habilidades_tecnicas import CategoriaHabilidadTecnica, HabilidadTecnica
from app.schemas.habilidades_tecnicas import HabilidadTecnicaCreate, CategoriaHabilidadTecnicaCreate

# Obtener todas las categorías de habilidades técnicas
def get_categorias_habilidades(db: Session):
    return db.query(CategoriaHabilidadTecnica).all()

# Obtener una categoría específica por ID
def get_categoria_habilidad(db: Session, categoria_id: int):
    categoria = db.query(CategoriaHabilidadTecnica).filter(CategoriaHabilidadTecnica.id_categoria_habilidad == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría de habilidad técnica no encontrada")
    return categoria

# Crear una nueva categoría de habilidades técnicas
def create_categoria_habilidad(db: Session, categoria_data: CategoriaHabilidadTecnicaCreate):
    categoria_existente = db.query(CategoriaHabilidadTecnica).filter(CategoriaHabilidadTecnica.nombre_categoria == categoria_data.nombre_categoria).first()
    if categoria_existente:
        raise HTTPException(status_code=400, detail="Ya existe una categoría con este nombre")
    
    nueva_categoria = CategoriaHabilidadTecnica(nombre_categoria=categoria_data.nombre_categoria)
    db.add(nueva_categoria)
    db.commit()
    db.refresh(nueva_categoria)
    return nueva_categoria

def update_categoria_habilidad(db: Session, categoria_id: int, categoria_data: CategoriaHabilidadTecnicaCreate):
    categoria = db.query(CategoriaHabilidadTecnica).filter(CategoriaHabilidadTecnica.id_categoria_habilidad == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría de habilidad técnica no encontrada")
    
    categoria.nombre_categoria = categoria_data.nombre_categoria
    db.commit()
    db.refresh(categoria)
    return categoria


def delete_categoria_habilidad(db: Session, categoria_id: int):
    categoria = db.query(CategoriaHabilidadTecnica).filter(CategoriaHabilidadTecnica.id_categoria_habilidad == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría de habilidad técnica no encontrada")
    
    # Verificar si tiene habilidades asociadas
    if categoria.habilidades_tecnicas:
        raise HTTPException(status_code=400, detail="No se puede eliminar una categoría con habilidades técnicas asociadas")

    db.delete(categoria)
    db.commit()
    return {"message": "Categoría de habilidad técnica eliminada exitosamente"}




# Obtener todas las habilidades técnicas
def get_habilidades_tecnicas(db: Session):
    return db.query(HabilidadTecnica).all()

# Obtener una habilidad técnica específica por ID
def get_habilidad_tecnica(db: Session, habilidad_id: int):
    habilidad = db.query(HabilidadTecnica).filter(HabilidadTecnica.id_habilidad_tecnica == habilidad_id).first()
    if not habilidad:
        raise HTTPException(status_code=404, detail="Habilidad técnica no encontrada")
    return habilidad

# Crear una nueva habilidad técnica con posibilidad de crear también una nueva categoría
def create_habilidad_tecnica(db: Session, habilidad_data: HabilidadTecnicaCreate):
    # Validar si la habilidad ya existe
    habilidad_existente = db.query(HabilidadTecnica).filter(HabilidadTecnica.nombre_habilidad == habilidad_data.nombre_habilidad).first()
    if habilidad_existente:
        raise HTTPException(status_code=400, detail="Ya existe una habilidad con este nombre")

    # Si el usuario proporciona `nueva_categoria`, creamos una nueva categoría
    if habilidad_data.nueva_categoria:
        nueva_categoria = create_categoria_habilidad(db, habilidad_data.nueva_categoria)
        id_categoria = nueva_categoria.id_categoria_habilidad
    elif habilidad_data.id_categoria_habilidad:
        # Verificar si la categoría proporcionada existe
        categoria = get_categoria_habilidad(db, habilidad_data.id_categoria_habilidad)
        id_categoria = categoria.id_categoria_habilidad
    else:
        raise HTTPException(status_code=400, detail="Debe proporcionar una categoría válida o crear una nueva")

    nueva_habilidad = HabilidadTecnica(
        nombre_habilidad=habilidad_data.nombre_habilidad,
        id_categoria_habilidad=id_categoria
    )
    db.add(nueva_habilidad)
    db.commit()
    db.refresh(nueva_habilidad)
    return nueva_habilidad

# Actualizar una habilidad técnica
def update_habilidad_tecnica(db: Session, habilidad_id: int, habilidad_data: HabilidadTecnicaCreate):
    habilidad = get_habilidad_tecnica(db, habilidad_id)

    # Verificar si la habilidad con el nuevo nombre ya existe
    habilidad_existente = db.query(HabilidadTecnica).filter(
        HabilidadTecnica.nombre_habilidad == habilidad_data.nombre_habilidad,
        HabilidadTecnica.id_habilidad_tecnica != habilidad_id
    ).first()
    if habilidad_existente:
        raise HTTPException(status_code=400, detail="Ya existe otra habilidad con este nombre")

    # Si el usuario proporciona `nueva_categoria`, creamos una nueva categoría
    if habilidad_data.nueva_categoria:
        nueva_categoria = create_categoria_habilidad(db, habilidad_data.nueva_categoria)
        habilidad.id_categoria_habilidad = nueva_categoria.id_categoria_habilidad
    elif habilidad_data.id_categoria_habilidad:
        categoria = get_categoria_habilidad(db, habilidad_data.id_categoria_habilidad)
        habilidad.id_categoria_habilidad = categoria.id_categoria_habilidad

    habilidad.nombre_habilidad = habilidad_data.nombre_habilidad
    db.commit()
    db.refresh(habilidad)
    return habilidad

# Eliminar una habilidad técnica
def delete_habilidad_tecnica(db: Session, habilidad_id: int):
    habilidad = get_habilidad_tecnica(db, habilidad_id)
    db.delete(habilidad)
    db.commit()
    return {"message": "Habilidad técnica eliminada correctamente"}
