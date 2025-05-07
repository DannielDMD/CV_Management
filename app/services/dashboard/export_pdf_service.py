# services/dashboard/export_pdf_service.py

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
# Importamos tu nuevo service de proceso
from app.services.dashboard.stats_proceso_service import obtener_estadisticas_proceso

def exportar_estadisticas_pdf_reportlab(
    db: Session,
    año: Optional[int] = None
) -> BytesIO:
    """
    Genera un PDF con todas las estadísticas por sección usando ReportLab:
      - Personal
      - Educación
      - Experiencia
      - Conocimientos
      - Preferencias
      - Proceso (nuevo service)
    Retorna un BytesIO listo para enviar como StreamingResponse.
    """

    # Obtener datos de cada sección
    personal       = obtener_estadisticas_personales(db, año)
    educacion      = obtener_estadisticas_educacion(db, año)
    experiencia    = obtener_estadisticas_experiencia(db, año)
    conocimientos  = obtener_estadisticas_conocimientos(db, año)
    preferencias    = obtener_estadisticas_preferencias(db, año)
    proceso        = obtener_estadisticas_proceso(db, año)

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Logo y encabezado
    elements.append(Image("app/static/LogoJoyco.png", width=100, height=50))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Reporte de Estadísticas", styles["Title"]))
    elements.append(Paragraph(f"Generado: {datetime.now():%Y-%m-%d %H:%M:%S}", styles["Normal"]))
    if año:
        elements.append(Paragraph(f"Año filtrado: {año}", styles["Normal"]))
    elements.append(Spacer(1, 24))

    def add_section(title, rows):
        elements.append(Paragraph(title, styles["Heading2"]))
        if not rows:
            elements.append(Paragraph("Sin datos disponibles.", styles["Normal"]))
        else:
            table_data = [["Etiqueta", "Cantidad"], *rows]
            tbl = Table(table_data, colWidths=[300, 100])
            tbl.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ]))
            elements.append(tbl)
        elements.append(Spacer(1, 12))

    # ─ Sección Personal ─
    add_section("Top Ciudades (anual)", [(i.label, i.count) for i in personal.top_ciudades_anual])
    add_section("Top Cargos (anual)", [(i.label, i.count) for i in personal.top_cargos_anual])
    add_section("Rangos de edad",       [(i.label, i.count) for i in personal.rangos_edad])
    add_section("Estados de candidatos",[(i.label, i.count) for i in personal.estado_candidatos])
    add_section("Booleanos", [
        ("Referidos",              personal.estadisticas_booleanas.referidos),
        ("No referidos",           personal.estadisticas_booleanas.no_referidos),
        ("Formularios completos",  personal.estadisticas_booleanas.formularios_completos),
        ("Formularios incompletos",personal.estadisticas_booleanas.formularios_incompletos),
        ("Trabaja en Joyco",       personal.estadisticas_booleanas.trabaja_actualmente_joyco),
        ("Ha trabajado en Joyco",  personal.estadisticas_booleanas.ha_trabajado_joyco),
    ])

    # ─ Sección Educación ─
    add_section("Top niveles educativos",     [(i.label, i.count) for i in educacion.top_niveles_educacion_anual])
    add_section("Top títulos obtenidos",      [(i.label, i.count) for i in educacion.top_titulos_obtenidos_anual])
    add_section("Top instituciones",          [(i.label, i.count) for i in educacion.top_instituciones_academicas_anual])
    add_section("Nivel de inglés",            [(i.label, i.count) for i in educacion.distribucion_nivel_ingles_anual])

    # ─ Sección Experiencia ─
    add_section("Top rangos de experiencia",  [(i.label, i.count) for i in experiencia.top_rangos_experiencia_anual])
    add_section("Top últimos cargos",         [(i.label, i.count) for i in experiencia.top_ultimos_cargos_anual])
    add_section("Top últimas empresas",       [(i.label, i.count) for i in experiencia.top_ultimas_empresas_anual])
    add_section("Duración experiencia",       [(i.label, i.count) for i in experiencia.distribucion_duracion])

    # ─ Sección Conocimientos ─
    add_section("Habilidades blandas",       [(i.label, i.count) for i in conocimientos.top_habilidades_blandas_anual])
    add_section("Habilidades técnicas",      [(i.label, i.count) for i in conocimientos.top_habilidades_tecnicas_anual])
    add_section("Herramientas",              [(i.label, i.count) for i in conocimientos.top_herramientas_anual])

    # ─ Sección Preferencias ─
    add_section("Disponibilidad inicio",     [(i.label, i.count) for i in preferencias.top_disponibilidad_inicio_anual])
    add_section("Rangos salariales",         [(i.label, i.count) for i in preferencias.top_rangos_salariales_anual])
    add_section("Motivos de salida",         [(i.label, i.count) for i in preferencias.top_motivos_salida_anual])
    add_section("Viajar",                    [(i.label, i.count) for i in preferencias.disponibilidad_viajar_anual])
    add_section("Situación laboral",         [(i.label, i.count) for i in preferencias.situacion_laboral_actual_anual])

    # ─ Sección Proceso ─
    # 1) Candidatos por mes
    add_section(
        "Candidatos por mes",
        [(f"Mes {m.month}", m.count) for m in proceso.candidatos_por_mes]
    )
    # 2) Top estados anual
    add_section(
        "Top estados (anual)",
        [(e.label, e.count) for e in proceso.top_estados_anual]
    )
    # 3) Top estado por mes
    add_section(
        "Top estado por mes",
        [(f"Mes {t.month}: {t.label}", t.count) for t in proceso.top_estados_por_mes]
    )

    # Construir y devolver
    doc.build(elements)
    buffer.seek(0)
    return buffer
