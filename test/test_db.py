from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.candidato import Ciudad, CargoOfrecido, CategoriaCargo, Candidato
from app.models.educacion import Educacion, NivelEducacion, TituloObtenido, InstitucionAcademica, NivelIngles
from app.models.experiencia import ExperienciaLaboral, RangoExperiencia
from app.models.preferencias import RangoSalarial, Disponibilidad, MotivoSalida
from app.models.habilidades_blandas import *
from app.models.habilidades_tecnicas import *
from app.models. herramientas import *
router = APIRouter()


#Rutas de Candidato
@router.get("/candidatos") 
def get_candidatos(db: Session = Depends(get_db)):
    return db.query(Candidato).all()

@router.get("/ciudades")  
def get_ciudades(db: Session = Depends(get_db)):
    return db.query(Ciudad).all()

@router.get("/categorias-cargos")
def get_cargos (db: Session = Depends(get_db)):
    return db.query(CategoriaCargo).all()

@router.get("/cargos")
def get_cargos (db: Session = Depends(get_db)):
    return db.query(CargoOfrecido).all()


#EDUCACION
@router.get("/educacion") 
def get_educacion(db: Session = Depends(get_db)):
    return db.query(Educacion).all()

@router.get("/nivel") 
def get_educacion(db: Session = Depends(get_db)):
    return db.query(NivelEducacion).all()

@router.get("/titulo") 
def get_educacion(db: Session = Depends(get_db)):
    return db.query(TituloObtenido).all()

@router.get("/institucion") 
def get_educacion(db: Session = Depends(get_db)):
    return db.query(InstitucionAcademica).all()

@router.get("/ingles") 
def get_educacion(db: Session = Depends(get_db)):
    return db.query(NivelIngles).all()


# EXPERIENCIA

@router.get("/experiencia") 
def get_educacion(db: Session = Depends(get_db)):
    return db.query(ExperienciaLaboral).all()

@router.get("/rangos") 
def get_educacion(db: Session = Depends(get_db)):
    return db.query(RangoExperiencia).all()


# HABILIDADES Y HERRAMIENTAS

@router.get("/habilidades_blandas") 
def get_educacion(db: Session = Depends(get_db)):
    return db.query(HabilidadBlanda).all()

@router.get("/habilidad_blanda_candidato") 
def get_educacion(db: Session = Depends(get_db)):
    return db.query(HabilidadBlandaCandidato).all()

@router.get("/habilidad_tecnica") 
def get_educacion(db: Session = Depends(get_db)):
    return db.query(HabilidadTecnica).all()

@router.get("/cate_hab_tec") 
def get_educacion(db: Session = Depends(get_db)):
    return db.query(CategoriaHabilidadTecnica).all()

@router.get("/habilidad_candidato") 
def get_educacion(db: Session = Depends(get_db)):
    return db.query(HabilidadTecnicaCandidato).all()

@router.get("/herramientas") 
def get_educacion(db: Session = Depends(get_db)):
    return db.query(Herramienta).all()

@router.get("/cate_herra") 
def get_educacion(db: Session = Depends(get_db)):
    return db.query(CategoriaHerramienta).all()

@router.get("/herr_candidadato") 
def get_educacion(db: Session = Depends(get_db)):
    return db.query(HerramientaCandidato).all()

# PREFERENCIAS

@router.get("/preferencias")
def get_educacion(db: Session = Depends(get_db)):
    return db.query(Disponibilidad).all()

@router.get("/rangos_salariales") 
def get_educacion(db: Session = Depends(get_db)):
    return db.query(RangoSalarial).all()

@router.get("/motivo") 
def get_educacion(db: Session = Depends(get_db)):
    return db.query(MotivoSalida).all()

