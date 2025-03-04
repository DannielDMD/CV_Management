from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.candidato import Candidato
from app.schemas.candidato import CandidatoCreate, CandidatoUpdate
from fastapi import HTTPException

# Crear un candidato
def create_candidato(db: Session, candidato_data: CandidatoCreate):
    # Verificar si el correo ya existe
    existing_candidato = db.query(Candidato).filter(Candidato.correo_electronico == candidato_data.correo_electronico).first()
    if existing_candidato:
        raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado")

    # Crear instancia del modelo con los datos recibidos
    nuevo_candidato = Candidato(**candidato_data.model_dump())

    try:
        db.add(nuevo_candidato)
        db.commit()
        db.refresh(nuevo_candidato)
        return nuevo_candidato
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al insertar el candidato en la base de datos")

def get_candidato_by_id(db: Session, id_candidato: int):
    candidato = db.query(Candidato).filter(Candidato.id_candidato == id_candidato).first()
    
    if not candidato:
        raise HTTPException(status_code=404, detail="Candidato no encontrado")

    return candidato  #FastAPI lo serializa automáticamente

#  Obtener todos los candidatos
def get_all_candidatos(db: Session):
    return db.query(Candidato).all()

# Actualizar un candidato
def update_candidato(db: Session, id_candidato: int, candidato_data: CandidatoUpdate):
    candidato = db.query(Candidato).filter(Candidato.id_candidato == id_candidato).first()
    if not candidato:
        raise HTTPException(status_code=404, detail="Candidato no encontrado")

    # Actualizar solo los campos que se envían en la solicitud
    for key, value in candidato_data.model_dump(exclude_unset=True).items():
        setattr(candidato, key, value)

    db.commit()
    db.refresh(candidato)
    return candidato

#  Eliminar un candidato
def delete_candidato(db: Session, id_candidato: int):
    candidato = db.query(Candidato).filter(Candidato.id_candidato == id_candidato).first()
    if not candidato:
        raise HTTPException(status_code=404, detail="Candidato no encontrado")

    db.delete(candidato)
    db.commit()
    return {"message": "Candidato eliminado correctamente"}

"""
📌 Explicación rápida de cada función
create_candidato(db, candidato_data)

Verifica si el correo ya existe en la base de datos.
Si no existe, crea un nuevo candidato y lo guarda en la BD.
get_candidato_by_id(db, id_candidato)

Busca un candidato por su ID.
Si no lo encuentra, devuelve un error 404.
get_all_candidatos(db)

Devuelve todos los candidatos almacenados en la BD.
update_candidato(db, id_candidato, candidato_data)

Busca el candidato por ID.
Actualiza solo los campos que el usuario envíe (no reemplaza valores existentes con None).
delete_candidato(db, id_candidato)

Busca el candidato por ID.
Si existe, lo elimina de la base de datos.
"""