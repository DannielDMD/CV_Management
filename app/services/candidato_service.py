from datetime import datetime, timedelta, timezone
import logging
from typing import Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc, extract, func, or_
from fastapi import HTTPException
from app.models.candidato_model import Candidato
from app.models.catalogs.ciudad import Ciudad
from app.schemas.candidato_schema import (
    CandidatoCreate,
    CandidatoUpdate,
    CandidatoResumenResponse,
    CandidatoDetalleResponse,
)
from app.models.educacion_model import Educacion
from app.models.experiencia_model import ExperienciaLaboral
from app.models.conocimientos_model import CandidatoConocimiento
from app.models.preferencias import PreferenciaDisponibilidad
from app.models.catalogs.cargo_ofrecido import CargoOfrecido



# Configurar logging
logger = logging.getLogger(__name__)


def create_candidato(db: Session, candidato_data: CandidatoCreate):
    """
    Crea un nuevo candidato en la base de datos.

    Validaciones:
    - Verifica si el correo electrónico ya existe en la base de datos.
    
    Pasos:
    1. Verifica la unicidad del correo.
    2. Si no existe, crea una instancia del modelo `Candidato`.
    3. Agrega el nuevo candidato a la sesión de la base de datos.
    4. Hace commit de la sesión y refresca para obtener el ID generado.

    Args:
        db (Session): Sesión activa de SQLAlchemy.
        candidato_data (CandidatoCreate): Datos del candidato recibidos desde el frontend.

    Returns:
        Candidato: Objeto candidato recién creado, incluyendo su ID.

    Raises:
        HTTPException: 
            - 400 si el correo ya está registrado.
            - 500 si ocurre un error de integridad al guardar en la base de datos.
    """
    if (
        db.query(Candidato)
        .filter(Candidato.correo_electronico == candidato_data.correo_electronico)
        .first()
    ):
        raise HTTPException(
            status_code=400, detail="El correo electrónico ya está registrado"
        )

    campos = candidato_data.model_dump()
    nuevo_candidato = Candidato(**campos)


    try:
        db.add(nuevo_candidato)
        db.commit()
        db.refresh(nuevo_candidato)  # 🔥 Esto recupera el ID generado
        print(f"Nuevo ID generado: {nuevo_candidato.id_candidato}")  # ✅ Debug
        return nuevo_candidato
    except IntegrityError as e:
        logger.error(f"Error de integridad al insertar candidato: {e}")
        db.rollback()
        raise HTTPException(
            status_code=500, detail="Error al insertar el candidato en la base de datos"
        )



def get_candidato_by_id(db: Session, id_candidato: int):
    """
    Recupera un candidato específico por su ID.

    Args:
        db (Session): Sesión activa de SQLAlchemy.
        id_candidato (int): ID del candidato a buscar.

    Returns:
        Candidato: Objeto del candidato encontrado.

    Raises:
        HTTPException: 404 si no se encuentra el candidato.
    """
    candidato = db.get(Candidato, id_candidato)
    if not candidato:
        raise HTTPException(status_code=404, detail="Candidato no encontrado")
    return candidato

def get_all_candidatos(db: Session):
    """
    Recupera todos los candidatos registrados en la base de datos.

    Args:
        db (Session): Sesión activa de SQLAlchemy.

    Returns:
        List[Candidato]: Lista de todos los candidatos.
    """
    return db.query(Candidato).all()

def update_candidato(db: Session, id_candidato: int, candidato_data: CandidatoUpdate):
    """
    Actualiza los datos de un candidato existente.

    Args:
        db (Session): Sesión activa de SQLAlchemy.
        id_candidato (int): ID del candidato a actualizar.
        candidato_data (CandidatoUpdate): Datos nuevos a aplicar.

    Returns:
        Candidato: Objeto candidato actualizado.

    Raises:
        HTTPException:
            - 404 si no se encuentra el candidato.
            - 400 si no hay datos para actualizar.
            - 500 si ocurre un error al guardar los cambios.
    """
    candidato = db.get(Candidato, id_candidato)
    print("Campos a actualizar:", cambios)  # Puedes quitarlo en producción
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
        raise HTTPException(
            status_code=500,
            detail="Error al actualizar el candidato en la base de datos",
        )

def delete_candidato(db: Session, id_candidato: int):
    """
    Elimina un candidato de la base de datos por su ID.

    Args:
        db (Session): Sesión activa de SQLAlchemy.
        id_candidato (int): ID del candidato a eliminar.

    Returns:
        dict: Mensaje de confirmación.

    Raises:
        HTTPException:
            - 404 si no se encuentra el candidato.
            - 500 si ocurre un error al eliminar el registro.
    """
    candidato = db.get(Candidato, id_candidato)
    if not candidato:
        raise HTTPException(status_code=404, detail="Candidato no encontrado")

    db.delete(candidato)
    try:
        db.commit()
        return {
            "message": f"Candidato {candidato.nombre_completo} eliminado correctamente"
        }
    except Exception as e:
        logger.error(f"Error al eliminar candidato: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al eliminar el candidato")


def get_candidatos_resumen(
    db: Session,
    search: str = None,
    estado: str = None,
    id_disponibilidad: int = None,
    id_cargo: int = None,
    id_ciudad: int = None,
    id_herramienta: int = None,
    id_habilidad_tecnica: int = None,
    id_nivel_ingles: int = None,
    id_experiencia: int = None,
    id_titulo: int = None,
    trabaja_joyco: bool = None,
    ordenar_por_fecha: Optional[str] = None,
    anio: Optional[int] = None,
    mes: Optional[int] = None,
    skip: int = 0,
    limit: int = 10,
):
    """
    Obtiene un resumen paginado de candidatos, aplicando múltiples filtros opcionales.

    Esta función construye una consulta dinámica a partir de filtros como:
    - texto de búsqueda (nombre, correo o cargo)
    - estado del proceso
    - disponibilidad, ciudad, cargo ofrecido
    - herramientas, habilidades, título, inglés, experiencia
    - si trabaja en Joyco actualmente
    - año y mes de postulación
    También permite ordenar por fecha y aplicar paginación.

    Args:
        db (Session): Sesión de base de datos.
        search (str): Término de búsqueda general.
        estado (str): Estado del candidato (ej. "ADMITIDO", "DESCARTADO").
        id_disponibilidad (int): ID del tipo de disponibilidad.
        id_cargo (int): ID del cargo ofrecido.
        id_ciudad (int): ID de la ciudad.
        id_herramienta (int): ID de la herramienta específica.
        id_habilidad_tecnica (int): ID de habilidad técnica.
        id_nivel_ingles (int): ID del nivel de inglés.
        id_experiencia (int): ID del rango de experiencia.
        id_titulo (int): ID del título académico.
        trabaja_joyco (bool): Si el candidato trabaja actualmente en Joyco.
        ordenar_por_fecha (str): "recientes" o "antiguos".
        anio (int): Año de postulación (filtro por fecha_registro).
        mes (int): Mes de postulación (filtro por fecha_registro).
        skip (int): Número de elementos a omitir (paginación).
        limit (int): Número máximo de elementos a retornar.

    Returns:
        dict: Un diccionario con:
            - data: lista de candidatos resumidos
            - total: cantidad total de registros sin paginar

    Raises:
        No genera errores directamente salvo que se rompa la conexión con DB.
    """


    query = db.query(Candidato).options(
        joinedload(Candidato.ciudad),
        joinedload(Candidato.cargo),
        joinedload(Candidato.educaciones).joinedload(Educacion.nivel_educacion),
        joinedload(Candidato.educaciones).joinedload(Educacion.titulo),
        joinedload(Candidato.experiencias).joinedload(
            ExperienciaLaboral.rango_experiencia
        ),
        joinedload(Candidato.conocimientos).joinedload(
            CandidatoConocimiento.habilidad_blanda
        ),
        joinedload(Candidato.conocimientos).joinedload(
            CandidatoConocimiento.habilidad_tecnica
        ),
        joinedload(Candidato.conocimientos).joinedload(
            CandidatoConocimiento.herramienta
        ),
        joinedload(Candidato.preferencias).joinedload(
            PreferenciaDisponibilidad.disponibilidad
        ),
    )

    # Filtros
    if search:
        query = query.join(Candidato.cargo).filter(
            or_(
                Candidato.nombre_completo.ilike(f"%{search}%"),
                Candidato.correo_electronico.ilike(f"%{search}%"),
                CargoOfrecido.nombre_cargo.ilike(f"%{search}%"),
            )
        )
    if estado:
        query = query.filter(Candidato.estado == estado)
    if id_disponibilidad:
        query = query.join(Candidato.preferencias).filter(
            PreferenciaDisponibilidad.id_disponibilidad == id_disponibilidad
        )
    if id_cargo:
        query = query.filter(Candidato.id_cargo == id_cargo)
    if id_ciudad:
        query = query.filter(Candidato.id_ciudad == id_ciudad)
    if trabaja_joyco is not None:
        query = query.filter(Candidato.trabaja_actualmente_joyco == trabaja_joyco)
    if id_herramienta:
        query = query.join(Candidato.conocimientos).filter(
            CandidatoConocimiento.id_herramienta == id_herramienta
        )
    if id_habilidad_tecnica:
        query = query.join(Candidato.conocimientos).filter(
            CandidatoConocimiento.id_habilidad_tecnica == id_habilidad_tecnica
        )
    if id_titulo:
        query = query.join(Candidato.educaciones).filter(
            Educacion.id_titulo == id_titulo
        )
    if id_nivel_ingles:
        query = query.join(Candidato.educaciones).filter(
            Educacion.id_nivel_ingles == id_nivel_ingles
        )
    if id_experiencia:
        query = query.join(Candidato.experiencias).filter(
            ExperienciaLaboral.id_rango_experiencia == id_experiencia
        )
    
    if anio:
        query = query.filter(extract("year", Candidato.fecha_registro) == anio)

    if mes:
        query = query.filter(extract("month", Candidato.fecha_registro) == mes)


    # Cálculo antes del paginado
    total = query.count()

    # Aplicar ordenamiento si se solicitó
    if ordenar_por_fecha == "recientes":
        query = query.order_by(desc(Candidato.fecha_registro))
    elif ordenar_por_fecha == "antiguos":
        query = query.order_by(Candidato.fecha_registro)

    # aplicar paginación
    candidatos = query.offset(skip).limit(limit).all()

    # Lógica para armar el resumen
    resumen = []
    for candidato in candidatos:
        educacion = candidato.educaciones[0] if candidato.educaciones else None
        experiencia = candidato.experiencias[0] if candidato.experiencias else None
        preferencias = candidato.preferencias[0] if candidato.preferencias else None

        habilidades_blandas = []
        habilidades_tecnicas = []
        herramientas = []

        for c in candidato.conocimientos:
            if c.tipo_conocimiento == "blanda" and c.habilidad_blanda:
                habilidades_blandas.append(c.habilidad_blanda.nombre_habilidad_blanda)
            elif c.tipo_conocimiento == "tecnica" and c.habilidad_tecnica:
                habilidades_tecnicas.append(
                    c.habilidad_tecnica.nombre_habilidad_tecnica
                )
            elif c.tipo_conocimiento == "herramienta" and c.herramienta:
                herramientas.append(c.herramienta.nombre_herramienta)

        resumen.append(
            CandidatoResumenResponse(
                id_candidato=candidato.id_candidato,
                nombre_completo=candidato.nombre_completo,
                correo_electronico=candidato.correo_electronico,
                telefono=candidato.telefono,
                ciudad=candidato.ciudad.nombre_ciudad,
                cargo_ofrecido=candidato.cargo.nombre_cargo,
                nivel_educativo=(
                    educacion.nivel_educacion.descripcion_nivel if educacion else None
                ),
                titulo_obtenido=(
                    educacion.titulo.nombre_titulo
                    if educacion and educacion.titulo
                    else None
                ),
                rango_experiencia=(
                    experiencia.rango_experiencia.descripcion_rango
                    if experiencia
                    else None
                ),
                habilidades_blandas=habilidades_blandas,
                habilidades_tecnicas=habilidades_tecnicas,
                herramientas=herramientas,
                disponibilidad_inicio=(
                    preferencias.disponibilidad.descripcion_disponibilidad
                    if preferencias
                    else None
                ),
                trabaja_actualmente_joyco=candidato.trabaja_actualmente_joyco,
                fecha_postulacion=candidato.fecha_registro,
                estado=candidato.estado,
            )
        )

    # Retorno del total
    return {"data": resumen, "total": total}


# -------------Detalle de un Candidato -----------------#
def get_candidato_detalle(db: Session, id_candidato: int) -> CandidatoDetalleResponse:
    """
    Retorna el detalle completo de un candidato específico por su ID.

    Esta función recupera la información personal, educativa, laboral, de conocimientos y de preferencias
    de un candidato, usando múltiples joins para evitar llamadas adicionales a la base de datos.

    Args:
        db (Session): Sesión activa de la base de datos.
        id_candidato (int): ID único del candidato a consultar.

    Returns:
        CandidatoDetalleResponse: Objeto con todos los datos consolidados del candidato.

    Raises:
        HTTPException: Si no se encuentra un candidato con el ID proporcionado (404).
    
    Estructura del objeto retornado:
        - Información personal (nombre, correo, cédula, ciudad, cargo, estado, etc.)
        - Educación (nivel, título, institución, año, inglés)
        - Experiencia laboral (empresa, cargo, funciones, duración)
        - Conocimientos (habilidades blandas, técnicas, herramientas)
        - Preferencias (disponibilidad, salario, motivo de salida, razón para trabajar)
    """
    candidato = (
        db.query(Candidato)
        .options(
            joinedload(Candidato.ciudad).joinedload(Ciudad.departamento),
            joinedload(Candidato.cargo),
            joinedload(Candidato.centro_costos),
            joinedload(Candidato.motivo_salida),
            # Joins de Educación
            joinedload(Candidato.educaciones).joinedload(Educacion.nivel_educacion),
            joinedload(Candidato.educaciones).joinedload(Educacion.titulo),
            joinedload(Candidato.educaciones).joinedload(Educacion.institucion),
            joinedload(Candidato.educaciones).joinedload(Educacion.nivel_ingles),
            # Joins de Experiencia
            joinedload(Candidato.experiencias).joinedload(
                ExperienciaLaboral.rango_experiencia
            ),
            # Joins de Conocimientos
            joinedload(Candidato.conocimientos).joinedload(
                CandidatoConocimiento.habilidad_blanda
            ),
            joinedload(Candidato.conocimientos).joinedload(
                CandidatoConocimiento.habilidad_tecnica
            ),
            joinedload(Candidato.conocimientos).joinedload(
                CandidatoConocimiento.herramienta
            ),
            # Joins de Preferencias
            joinedload(Candidato.preferencias).joinedload(
                PreferenciaDisponibilidad.disponibilidad
            ),
            joinedload(Candidato.preferencias).joinedload(
                PreferenciaDisponibilidad.rango_salarial
            ),
            joinedload(Candidato.preferencias).joinedload(
                PreferenciaDisponibilidad.motivo_salida
            ),
        )
        .filter(Candidato.id_candidato == id_candidato)
        .first()
    )
    # Verifica si el candidato existe
    if not candidato:
        raise HTTPException(status_code=404, detail="Candidato no encontrado")
    # Extrae una sola entrada por cada relación de uno-a-muchos
    educacion = candidato.educaciones[0] if candidato.educaciones else None
    experiencia = candidato.experiencias[0] if candidato.experiencias else None
    preferencias = candidato.preferencias[0] if candidato.preferencias else None
    # Separa las habilidades y herramientas según su tipo
    habilidades_blandas = [
        c.habilidad_blanda.nombre_habilidad_blanda
        for c in candidato.conocimientos
        if c.tipo_conocimiento == "blanda" and c.habilidad_blanda
    ]
    habilidades_tecnicas = [
        c.habilidad_tecnica.nombre_habilidad_tecnica
        for c in candidato.conocimientos
        if c.tipo_conocimiento == "tecnica" and c.habilidad_tecnica
    ]
    herramientas = [
        c.herramienta.nombre_herramienta
        for c in candidato.conocimientos
        if c.tipo_conocimiento == "herramienta" and c.herramienta
    ]
    # Construye la respuesta detallada del candidato combinando todas las secciones
    return CandidatoDetalleResponse(
        # Información Personal
        nombre_completo=candidato.nombre_completo,
        correo_electronico=candidato.correo_electronico,
        cc=candidato.cc,
        fecha_nacimiento=candidato.fecha_nacimiento,
        telefono=candidato.telefono,
        ciudad=candidato.ciudad.nombre_ciudad,
        departamento=(
        candidato.ciudad.departamento.nombre_departamento
        if candidato.ciudad and candidato.ciudad.departamento
        else None
        ),
        descripcion_perfil=candidato.descripcion_perfil,
        cargo=candidato.cargo.nombre_cargo,

        nombre_cargo_otro=candidato.nombre_cargo_otro,
        nombre_centro_costos_otro=candidato.nombre_centro_costos_otro,
        otro_motivo_salida=candidato.otro_motivo_salida,
        centro_costos=(candidato.centro_costos.nombre_centro_costos if candidato.centro_costos else None),
        trabaja_actualmente_joyco=candidato.trabaja_actualmente_joyco,
        ha_trabajado_joyco=candidato.ha_trabajado_joyco,
        motivo_salida=(
            candidato.motivo_salida.descripcion_motivo
            if candidato.motivo_salida
            else None
        ),
        tiene_referido=candidato.tiene_referido,
        nombre_referido=candidato.nombre_referido,
        fecha_registro=candidato.fecha_registro,
        estado=candidato.estado,
        # Educación
        nivel_educacion=(
            educacion.nivel_educacion.descripcion_nivel if educacion else None
        ),
        titulo=(
            educacion.titulo.nombre_titulo if educacion and educacion.titulo else None
        ),
        institucion=(
            educacion.institucion.nombre_institucion
            if educacion and educacion.institucion
            else None
        ),
        anio_graduacion=educacion.anio_graduacion if educacion else None,
        nivel_ingles=educacion.nivel_ingles.nivel if educacion else None,
        # Experiencia
        rango_experiencia=(
            experiencia.rango_experiencia.descripcion_rango if experiencia else None
        ),
        ultima_empresa=experiencia.ultima_empresa if experiencia else None,
        ultimo_cargo=experiencia.ultimo_cargo if experiencia else None,
        funciones=experiencia.funciones if experiencia else None,
        fecha_inicio=experiencia.fecha_inicio if experiencia else None,
        fecha_fin=experiencia.fecha_fin if experiencia else None,
        # Conocimientos
        habilidades_blandas=habilidades_blandas,
        habilidades_tecnicas=habilidades_tecnicas,
        herramientas=herramientas,
        # Preferencias
        disponibilidad_viajar=(
            preferencias.disponibilidad_viajar if preferencias else None
        ),
        disponibilidad_inicio=(
            preferencias.disponibilidad.descripcion_disponibilidad
            if preferencias
            else None
        ),
        rango_salarial=(
            preferencias.rango_salarial.descripcion_rango if preferencias else None
        ),
        trabaja_actualmente=preferencias.trabaja_actualmente if preferencias else None,
        motivo_salida_laboral=(
            preferencias.motivo_salida.descripcion_motivo
            if preferencias and preferencias.motivo_salida
            else None
        ),
        razon_trabajar_joyco=(
            preferencias.razon_trabajar_joyco if preferencias else None
        ),
    )

def obtener_estadisticas_candidatos(db: Session) -> dict:
    """
    Obtiene un resumen de candidatos agrupados por su estado actual dentro del proceso de selección.

    Returns:
        dict: Diccionario con el conteo por estado (e.g., 'EN_PROCESO', 'ADMITIDO') 
              e incluye una clave adicional 'total' con la suma de todos los registros.
    """
    resultados = (
        db.query(Candidato.estado, func.count(Candidato.id_candidato))
        .group_by(Candidato.estado)
        .all()
    )
    resumen = {estado: cantidad for estado, cantidad in resultados}
    resumen["total"] = sum(resumen.values())
    return resumen


def marcar_formulario_completo(db: Session, id_candidato: int) -> Candidato:
    """
    Marca el formulario de un candidato como completado, estableciendo el atributo 
    `formulario_completo` en True.

    Args:
        db (Session): Sesión activa de la base de datos.
        id_candidato (int): ID del candidato a actualizar.

    Returns:
        Candidato: Instancia actualizada del candidato.

    Raises:
        HTTPException: Si no se encuentra el candidato con el ID especificado.
    """
    candidato = db.query(Candidato).filter(Candidato.id_candidato == id_candidato).first()
    if not candidato:
        raise HTTPException(status_code=404, detail="Candidato no encontrado")

    candidato.formulario_completo = True
    db.commit()
    db.refresh(candidato)
    return candidato


def eliminar_candidatos_incompletos(db: Session) -> dict:
    """
    Elimina todos los candidatos cuyo formulario no ha sido completado y que fueron registrados 
    hace más de 6 horas.

    Args:
        db (Session): Sesión activa de la base de datos.

    Returns:
        dict: Diccionario con el número de registros eliminados bajo la clave 'eliminados'.
    """
    limite = datetime.now(timezone.utc) - timedelta(hours=6)
    candidatos = db.query(Candidato).filter(
        Candidato.formulario_completo == False,
        Candidato.fecha_registro < limite
    ).all()

    eliminados = 0
    for candidato in candidatos:
        db.delete(candidato)
        eliminados += 1

    db.commit()
    return {"eliminados": eliminados}   