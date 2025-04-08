import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.models.candidato_model import Candidato
from app.schemas.candidato_schema import CandidatoCreate, CandidatoResponse, CandidatoUpdate, CandidatoResumenResponse
from sqlalchemy.orm import Session, joinedload

from app.models.educacion_model import Educacion
from app.models.experiencia_model import ExperienciaLaboral
from app.models.conocimientos_model import CandidatoConocimiento
from app.models.preferencias import PreferenciaDisponibilidad





# Configurar logging
logger = logging.getLogger(__name__)

# Crear un candidato
def create_candidato(db: Session, candidato_data: CandidatoCreate):
    if db.query(Candidato).filter(Candidato.correo_electronico == candidato_data.correo_electronico).first():
        raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado")
    
    nuevo_candidato = Candidato(**candidato_data.model_dump())

    try:
        db.add(nuevo_candidato)
        db.commit()
        db.refresh(nuevo_candidato)  # 🔥 Esto recupera el ID generado
        print(f"Nuevo ID generado: {nuevo_candidato.id_candidato}")  # ✅ Debug
        return nuevo_candidato
    except IntegrityError as e:
        logger.error(f"Error de integridad al insertar candidato: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al insertar el candidato en la base de datos")

# Obtener un candidato por ID
def get_candidato_by_id(db: Session, id_candidato: int):
    candidato = db.get(Candidato, id_candidato)
    if not candidato:
        raise HTTPException(status_code=404, detail="Candidato no encontrado")
    return candidato

# Obtener todos los candidatos
def get_all_candidatos(db: Session):
    return db.query(Candidato).all()

# Actualizar un candidato
def update_candidato(db: Session, id_candidato: int, candidato_data: CandidatoUpdate):
    candidato = db.get(Candidato, id_candidato)
    if not candidato:
        raise HTTPException(status_code=404, detail="Candidato no encontrado")

    cambios = candidato_data.model_dump(exclude_unset=True)
    if not cambios:
        raise HTTPException(status_code=400, detail="No hay datos para actualizar")

    for key, value in cambios.items():
        setattr(candidato, key, value)

    try:
        db.commit()
        db.refresh(candidato)
        return candidato
    except IntegrityError as e:
        logger.error(f"Error al actualizar candidato: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al actualizar el candidato en la base de datos")

# Eliminar un candidato
def delete_candidato(db: Session, id_candidato: int):
    candidato = db.get(Candidato, id_candidato)
    if not candidato:
        raise HTTPException(status_code=404, detail="Candidato no encontrado")

    db.delete(candidato)
    try:
        db.commit()
        return {"message": f"Candidato {candidato.nombre_completo} eliminado correctamente"}
    except Exception as e:
        logger.error(f"Error al eliminar candidato: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al eliminar el candidato")
    
    
    #RESUMEN DE CANDIDATO
    
def get_candidatos_resumen(db: Session) -> list[CandidatoResumenResponse]:
    candidatos = db.query(Candidato).options(
        joinedload(Candidato.ciudad),
        joinedload(Candidato.cargo),
       joinedload(Candidato.educaciones).joinedload(Educacion.nivel_educacion),
joinedload(Candidato.educaciones).joinedload(Educacion.titulo),
        joinedload(Candidato.experiencias).joinedload(ExperienciaLaboral.rango_experiencia),
        joinedload(Candidato.conocimientos).joinedload(CandidatoConocimiento.habilidad_blanda),
        joinedload(Candidato.conocimientos).joinedload(CandidatoConocimiento.habilidad_tecnica),
        joinedload(Candidato.conocimientos).joinedload(CandidatoConocimiento.herramienta),
        joinedload(Candidato.preferencias).joinedload(PreferenciaDisponibilidad.disponibilidad)
    ).all()

    resumen = []

    for candidato in candidatos:
        educacion = candidato.educaciones[0] if candidato.educaciones else None
        experiencia = candidato.experiencias[0] if candidato.experiencias else None
        preferencias = candidato.preferencias[0] if candidato.preferencias else None

        # Clasificar conocimientos
        habilidades_blandas = []
        habilidades_tecnicas = []
        herramientas = []

        for c in candidato.conocimientos:
            if c.tipo_conocimiento == "blanda" and c.habilidad_blanda:
                habilidades_blandas.append(c.habilidad_blanda.nombre_habilidad_blanda)
            elif c.tipo_conocimiento == "tecnica" and c.habilidad_tecnica:
                habilidades_tecnicas.append(c.habilidad_tecnica.nombre_habilidad_tecnica)
            elif c.tipo_conocimiento == "herramienta" and c.herramienta:
                herramientas.append(c.herramienta.nombre_herramienta)

        resumen.append(CandidatoResumenResponse(
            id_candidato=candidato.id_candidato,
            nombre_completo=candidato.nombre_completo,
            correo_electronico=candidato.correo_electronico,
            telefono=candidato.telefono,
            ciudad=candidato.ciudad.nombre_ciudad,
            cargo_ofrecido=candidato.cargo.nombre_cargo,
            nivel_educativo=educacion.nivel_educacion.descripcion_nivel if educacion else None,
            titulo_obtenido=educacion.titulo.nombre_titulo if educacion and educacion.titulo else None,
            rango_experiencia=experiencia.rango_experiencia.descripcion_rango if experiencia else None,
            habilidades_blandas=habilidades_blandas,
            habilidades_tecnicas=habilidades_tecnicas,
            herramientas=herramientas,
            disponibilidad_inicio=preferencias.disponibilidad.descripcion_disponibilidad if preferencias else None,
            fecha_postulacion=candidato.fecha_registro,
            estado=candidato.estado
        ))

    return resumen