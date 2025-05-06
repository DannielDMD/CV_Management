# services/dashboard/export_service.py

from io import BytesIO
import pandas as pd
from sqlalchemy.orm import Session, joinedload

from app.models.candidato_model import Candidato
from app.models.educacion_model import Educacion
from app.models.experiencia_model import ExperienciaLaboral
from app.models.conocimientos_model import CandidatoConocimiento
from app.models.preferencias import PreferenciaDisponibilidad

def exportar_candidatos_detallados_excel(db: Session) -> BytesIO:
    """
    Genera un archivo Excel con toda la información detallada de cada candidato:
      - Datos personales
      - Educación
      - Experiencia laboral
      - Conocimientos
      - Preferencias y disponibilidad
    Retorna un BytesIO listo para enviar como StreamingResponse.
    """

    # 1. Consultar todos los candidatos con sus relaciones
    candidatos = (
        db.query(Candidato)
        .options(
            joinedload(Candidato.ciudad),
            joinedload(Candidato.cargo),
            joinedload(Candidato.motivo_salida),
            joinedload(Candidato.educaciones).joinedload(Educacion.nivel_educacion),
            joinedload(Candidato.educaciones).joinedload(Educacion.titulo),
            joinedload(Candidato.educaciones).joinedload(Educacion.institucion),
            joinedload(Candidato.educaciones).joinedload(Educacion.nivel_ingles),
            joinedload(Candidato.experiencias).joinedload(ExperienciaLaboral.rango_experiencia),
            joinedload(Candidato.conocimientos).joinedload(CandidatoConocimiento.habilidad_blanda),
            joinedload(Candidato.conocimientos).joinedload(CandidatoConocimiento.habilidad_tecnica),
            joinedload(Candidato.conocimientos).joinedload(CandidatoConocimiento.herramienta),
            joinedload(Candidato.preferencias).joinedload(PreferenciaDisponibilidad.disponibilidad),
            joinedload(Candidato.preferencias).joinedload(PreferenciaDisponibilidad.rango_salarial),
            joinedload(Candidato.preferencias).joinedload(PreferenciaDisponibilidad.motivo_salida),
        )
        .all()
    )

    # 2. Construir lista de diccionarios con todos los campos
    registros = []
    for c in candidatos:
        educ = c.educaciones[0] if c.educaciones else None
        exp = c.experiencias[0] if c.experiencias else None
        pref = c.preferencias[0] if c.preferencias else None

        hb = [
            ci.habilidad_blanda.nombre_habilidad_blanda
            for ci in c.conocimientos
            if ci.tipo_conocimiento == "blanda" and ci.habilidad_blanda
        ]
        ht = [
            ci.habilidad_tecnica.nombre_habilidad_tecnica
            for ci in c.conocimientos
            if ci.tipo_conocimiento == "tecnica" and ci.habilidad_tecnica
        ]
        hr = [
            ci.herramienta.nombre_herramienta
            for ci in c.conocimientos
            if ci.tipo_conocimiento == "herramienta" and ci.herramienta
        ]

        registros.append({
            "id_candidato": c.id_candidato,
            "nombre_completo": c.nombre_completo,
            "correo_electronico": c.correo_electronico,
            "cc": c.cc,
            "fecha_nacimiento": c.fecha_nacimiento,
            "telefono": c.telefono,
            "ciudad": c.ciudad.nombre_ciudad if c.ciudad else None,
            "descripcion_perfil": c.descripcion_perfil,
            "cargo": c.cargo.nombre_cargo if c.cargo else None,
            "trabaja_actualmente_joyco": c.trabaja_actualmente_joyco,
            "ha_trabajado_joyco": c.ha_trabajado_joyco,
            "motivo_salida": c.motivo_salida.descripcion_motivo if c.motivo_salida else None,
            "tiene_referido": c.tiene_referido,
            "nombre_referido": c.nombre_referido,
            "fecha_registro": c.fecha_registro,
            "estado": c.estado,
            "formulario_completo": c.formulario_completo,
            # Educación
            "nivel_educacion": educ.nivel_educacion.descripcion_nivel if educ else None,
            "titulo": educ.titulo.nombre_titulo if educ and educ.titulo else None,
            "institucion": educ.institucion.nombre_institucion if educ and educ.institucion else None,
            "anio_graduacion": educ.anio_graduacion if educ else None,
            "nivel_ingles": educ.nivel_ingles.nivel if educ and educ.nivel_ingles else None,
            # Experiencia
            "rango_experiencia": exp.rango_experiencia.descripcion_rango if exp else None,
            "ultima_empresa": exp.ultima_empresa if exp else None,
            "ultimo_cargo": exp.ultimo_cargo if exp else None,
            "funciones": exp.funciones if exp else None,
            "fecha_inicio": exp.fecha_inicio if exp else None,
            "fecha_fin": exp.fecha_fin if exp else None,
            # Conocimientos
            "habilidades_blandas": ", ".join(hb),
            "habilidades_tecnicas": ", ".join(ht),
            "herramientas": ", ".join(hr),
            # Preferencias
            "disponibilidad_viajar": pref.disponibilidad_viajar if pref else None,
            "disponibilidad_inicio": pref.disponibilidad.descripcion_disponibilidad if pref else None,
            "rango_salarial": pref.rango_salarial.descripcion_rango if pref else None,
            "trabaja_actualmente": pref.trabaja_actualmente if pref else None,
            "motivo_salida_laboral": pref.motivo_salida.descripcion_motivo if pref and pref.motivo_salida else None,
            "razon_trabajar_joyco": pref.razon_trabajar_joyco if pref else None,
        })

    # 3. Convertir a DataFrame
    df = pd.DataFrame(registros)

    # 4. Generar el Excel en memoria
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Candidatos")
    output.seek(0)

    return output
