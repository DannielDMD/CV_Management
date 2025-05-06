from io import BytesIO
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Table,
    TableStyle,
    Spacer,
    Image,
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from app.services.dashboard.stats_personal_service import obtener_estadisticas_personales
from app.services.dashboard.stats_educacion_service import obtener_estadisticas_educacion
from app.services.dashboard.stats_experiencia_service import obtener_estadisticas_experiencia
from app.services.dashboard.stats_conocimientos_service import obtener_estadisticas_conocimientos
from app.services.dashboard.stats_preferencias_service import obtener_estadisticas_preferencias
from app.services.candidato_service import obtener_estadisticas_candidatos as obtener_estadisticas_proceso

def exportar_estadisticas_pdf_reportlab(db: Session, año: Optional[int] = None) -> BytesIO:
    """
    Genera un PDF con todas las estadísticas por sección usando ReportLab:
      - Personal
      - Educación
      - Experiencia
      - Conocimientos
      - Preferencias
      - Proceso
    Retorna un BytesIO listo para enviar como StreamingResponse.
    """

    # Obtener datos de cada sección
    personal = obtener_estadisticas_personales(db, año)
    educacion = obtener_estadisticas_educacion(db, año)
    experiencia = obtener_estadisticas_experiencia(db, año)
    conocimientos = obtener_estadisticas_conocimientos(db, año)
    preferencias = obtener_estadisticas_preferencias(db, año)
    proceso = obtener_estadisticas_proceso(db, año)

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Logo y título
    logo_path = "app/static/LogoJoyco.png"
    elements.append(Image(logo_path, width=100, height=50))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Reporte de Estadísticas", styles["Title"]))
    fecha_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    elements.append(Paragraph(f"Generado: {fecha_str}", styles["Normal"]))
    if año:
        elements.append(Paragraph(f"Año filtrado: {año}", styles["Normal"]))
    elements.append(Spacer(1, 24))

    def add_section(title, data_rows):
        elements.append(Paragraph(title, styles["Heading2"]))
        if not data_rows:
            elements.append(Paragraph("Sin datos disponibles", styles["Normal"]))
            elements.append(Spacer(1, 12))
            return
        table_data = [["Etiqueta", "Cantidad"]] + data_rows
        table = Table(table_data, colWidths=[300, 100])
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ]
            )
        )
        elements.append(table)
        elements.append(Spacer(1, 12))

    # Sección: Información Personal
    add_section("Top Ciudades (Anual)", [(i.label, i.count) for i in personal.top_ciudades_anual])
    add_section("Top Cargos (Anual)", [(i.label, i.count) for i in personal.top_cargos_anual])
    add_section("Rangos de Edad", [(i.label, i.count) for i in personal.rangos_edad])
    add_section("Estado Candidatos", [(i.label, i.count) for i in personal.estado_candidatos])
    add_section("Campos Booleanos", [
        ("Ha trabajado en Joyco", personal.estadisticas_booleanas.ha_trabajado_joyco),
        ("Trabaja actualmente en Joyco", personal.estadisticas_booleanas.trabaja_actualmente_joyco),
        ("Formulario completo", personal.estadisticas_booleanas.formularios_completos),
        ("Tiene referido", personal.estadisticas_booleanas.referidos),
    ])

    # Sección: Educación
    add_section("Top Niveles Educativos", [(i.label, i.count) for i in educacion.top_niveles_educacion_anual])
    add_section("Top Títulos", [(i.label, i.count) for i in educacion.top_titulos_obtenidos_anual])
    add_section("Top Instituciones", [(i.label, i.count) for i in educacion.top_instituciones_academicas_anual])
    add_section("Distribución Nivel de Inglés", [(i.label, i.count) for i in educacion.distribucion_nivel_ingles_anual])

    # Sección: Experiencia
    add_section("Top Rangos de Experiencia", [(i.label, i.count) for i in experiencia.top_rangos_experiencia_anual])
    add_section("Top Últimos Cargos", [(i.label, i.count) for i in experiencia.top_ultimos_cargos_anual])
    add_section("Top Últimas Empresas", [(i.label, i.count) for i in experiencia.top_ultimas_empresas_anual])
    add_section("Distribución de Duración", [(i.label, i.count) for i in experiencia.distribucion_duracion])

    # Sección: Conocimientos
    add_section("Top Habilidades Blandas", [(i.label, i.count) for i in conocimientos.top_habilidades_blandas_anual])
    add_section("Top Habilidades Técnicas", [(i.label, i.count) for i in conocimientos.top_habilidades_tecnicas_anual])
    add_section("Top Herramientas", [(i.label, i.count) for i in conocimientos.top_herramientas_anual])

    # Sección: Preferencias
    add_section("Disponibilidad de Inicio", [(i.label, i.count) for i in preferencias.top_disponibilidad_inicio_anual])
    add_section("Rangos Salariales", [(i.label, i.count) for i in preferencias.top_rangos_salariales_anual])
    add_section("Motivos de Salida", [(i.label, i.count) for i in preferencias.top_motivos_salida_anual])
    add_section("Disponibilidad para Viajar", [(i.label, i.count) for i in preferencias.disponibilidad_viajar_anual])
    add_section("Situación Laboral Actual", [(i.label, i.count) for i in preferencias.situacion_laboral_actual_anual])

    # Sección: Proceso
    add_section("Estado en el Proceso", [(estado, count) for estado, count in proceso.items() if estado != "total"])

    # Generar PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer
