from typing import Optional
from io import BytesIO
import pandas as pd
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import extract
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl import Workbook
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.styles import Alignment

from app.models.candidato_model import Candidato
from app.models.educacion_model import Educacion
from app.models.experiencia_model import ExperienciaLaboral
from app.models.conocimientos_model import CandidatoConocimiento
from app.models.preferencias import PreferenciaDisponibilidad

def exportar_candidatos_detallados_excel(db: Session, año: Optional[int] = None) -> BytesIO:
    """
    Genera un archivo Excel con toda la información detallada de cada candidato.
    Si se especifica un año, solo se exportan los registrados ese año.
    """

    # 1. Consultar candidatos con joins
    query = (
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
    )
    if año:
        query = query.filter(extract("year", Candidato.fecha_registro) == año)

    candidatos = query.all()

    # 2. Construir registros
    registros = []
    for c in candidatos:
        educ = c.educaciones[0] if c.educaciones else None
        exp = c.experiencias[0] if c.experiencias else None
        pref = c.preferencias[0] if c.preferencias else None

        hb = [ci.habilidad_blanda.nombre_habilidad_blanda for ci in c.conocimientos if ci.tipo_conocimiento == "blanda" and ci.habilidad_blanda]
        ht = [ci.habilidad_tecnica.nombre_habilidad_tecnica for ci in c.conocimientos if ci.tipo_conocimiento == "tecnica" and ci.habilidad_tecnica]
        hr = [ci.herramienta.nombre_herramienta for ci in c.conocimientos if ci.tipo_conocimiento == "herramienta" and ci.herramienta]

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
            "estado": c.estado,
            "formulario_completo": c.formulario_completo,
            "acepta_politica_datos": c.acepta_politica_datos,
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
            # Fecha al final
            "fecha_registro": c.fecha_registro,
        })

    df = pd.DataFrame(registros)

    # Crear archivo Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Candidatos"

    if not df.empty:
        # Ordenar y mover columna
        df.sort_values(by="fecha_registro", ascending=False, inplace=True)
        columnas_ordenadas = [col for col in df.columns if col != "fecha_registro"] + ["fecha_registro"]
        df = df[columnas_ordenadas]

        # Escribir filas al worksheet
        for r_idx, row in enumerate(dataframe_to_rows(df, index=False, header=True), start=1):
            ws.append(row)
            for cell in ws[r_idx]:
                cell.alignment = Alignment(wrap_text=True, vertical="top")

        # Ajuste de anchos
        for col in ws.columns:
            max_length = max(len(str(cell.value or "")) for cell in col)
            ws.column_dimensions[col[0].column_letter].width = min(max_length + 2, 50)

        # Estilo de tabla
        tab = Table(displayName="TablaCandidatos", ref=ws.dimensions)
        style = TableStyleInfo(name="TableStyleMedium9", showRowStripes=True)
        tab.tableStyleInfo = style
        ws.add_table(tab)
    else:
        # Sin datos → mostrar mensaje
        ws.append(["Sin datos disponibles para el año seleccionado."])
        ws.column_dimensions["A"].width = 50
        ws["A1"].alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    # Guardar en BytesIO
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    return output

