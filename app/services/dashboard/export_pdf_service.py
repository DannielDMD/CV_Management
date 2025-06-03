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
# ───────────────────────── PERSONAL ─────────────────────────
    elements.append(Paragraph("📍 Estadísticas Personales", styles["Heading2"]))

    # Anuales
    add_section("Top ciudades (anual)", [(i.label, i.count) for i in personal.top_ciudades_anual])
    add_section("Top departamentos (anual)", [(i.label, i.count) for i in personal.top_departamentos_anual])
    add_section("Top centros de costos (anual)", [(i.label, i.count) for i in personal.top_centros_costos_anual])
    add_section("Top cargos (anual)", [(i.label, i.count) for i in personal.top_cargos_anual])
    add_section("Top nombres de referidos", [(i.label, i.count) for i in personal.top_nombres_referidos])
    add_section("Rangos de edad", [(i.label, i.count) for i in personal.rangos_edad])
    add_section("Estados de los candidatos", [(i.label, i.count) for i in personal.estado_candidatos])
    add_section("Estadísticas booleanas", [
        ("Referidos", personal.estadisticas_booleanas.referidos),
        ("No referidos", personal.estadisticas_booleanas.no_referidos),
        ("Formularios completos", personal.estadisticas_booleanas.formularios_completos),
        ("Formularios incompletos", personal.estadisticas_booleanas.formularios_incompletos),
        ("Trabaja en Joyco", personal.estadisticas_booleanas.trabaja_actualmente_joyco),
        ("Ha trabajado en Joyco", personal.estadisticas_booleanas.ha_trabajado_joyco),
    ])

    # Mensuales
    add_section("Candidatos registrados por mes", [(f"Mes {i.month}", i.count) for i in personal.candidatos_por_mes])
    add_section("Top ciudad por mes", [(f"Mes {i.month}: {i.label}", i.count) for i in personal.top_ciudades_por_mes])
    add_section("Top departamento por mes", [(f"Mes {i.month}: {i.label}", i.count) for i in personal.top_departamentos_por_mes])
    add_section("Top centro de costos por mes", [(f"Mes {i.month}: {i.label}", i.count) for i in personal.top_centros_costos_por_mes])
    add_section("Top cargo por mes", [(f"Mes {i.month}: {i.label}", i.count) for i in personal.top_cargos_por_mes])

# ───────────────────────── EDUCACIÓN ─────────────────────────
    elements.append(Paragraph("🎓 Estadísticas de Educación", styles["Heading2"]))

    # Anuales
    add_section("Top niveles educativos (anual)", [(i.label, i.count) for i in educacion.top_niveles_educacion_anual])
    add_section("Top títulos obtenidos (anual)", [(i.label, i.count) for i in educacion.top_titulos_obtenidos_anual])
    add_section("Top instituciones académicas (anual)", [(i.label, i.count) for i in educacion.top_instituciones_academicas_anual])
    add_section("Distribución del nivel de inglés (anual)", [(i.label, i.count) for i in educacion.distribucion_nivel_ingles_anual])
    add_section("Distribución por año de graduación", [(i.label, i.count) for i in educacion.distribucion_anio_graduacion])

    # Mensuales
    add_section("Educaciones registradas por mes", [(f"Mes {i.month}", i.count) for i in educacion.educaciones_por_mes])
    add_section("Top nivel educativo por mes", [(f"Mes {i.month}: {i.label}", i.count) for i in educacion.top_niveles_por_mes])
    add_section("Top título obtenido por mes", [(f"Mes {i.month}: {i.label}", i.count) for i in educacion.top_titulos_por_mes])
    add_section("Top institución académica por mes", [(f"Mes {i.month}: {i.label}", i.count) for i in educacion.top_instituciones_por_mes])
    add_section("Nivel de inglés más frecuente por mes", [(f"Mes {i.month}: {i.label}", i.count) for i in educacion.distribucion_nivel_ingles_por_mes])

    # ───────────────────────── EXPERIENCIA ────────────────────────
    elements.append(Paragraph("💼 Estadísticas de Experiencia", styles["Heading2"]))

    # Anuales
    add_section("Top rangos de experiencia (anual)", [(i.label, i.count) for i in experiencia.top_rangos_experiencia_anual])
    add_section("Top últimos cargos (anual)", [(i.label, i.count) for i in experiencia.top_ultimos_cargos_anual])
    add_section("Top últimas empresas (anual)", [(i.label, i.count) for i in experiencia.top_ultimas_empresas_anual])
    add_section("Distribución de duración de la experiencia", [(i.label, i.count) for i in experiencia.distribucion_duracion])

    # Mensuales
    add_section("Experiencias registradas por mes", [(f"Mes {i.month}", i.count) for i in experiencia.experiencias_por_mes])
    add_section("Top rango de experiencia por mes", [(f"Mes {i.month}: {i.label}", i.count) for i in experiencia.top_rangos_por_mes])
    add_section("Top último cargo por mes", [(f"Mes {i.month}: {i.label}", i.count) for i in experiencia.top_ultimos_cargos_por_mes])
    add_section("Top última empresa por mes", [(f"Mes {i.month}: {i.label}", i.count) for i in experiencia.top_ultimas_empresas_por_mes])
    
        # ───────────────────────── CONOCIMIENTOS ─────────────────────
    elements.append(Paragraph("🧠 Estadísticas de Conocimientos", styles["Heading2"]))

    # Anuales
    add_section("Top habilidades blandas (anual)", [(i.label, i.count) for i in conocimientos.top_habilidades_blandas_anual])
    add_section("Top habilidades técnicas (anual)", [(i.label, i.count) for i in conocimientos.top_habilidades_tecnicas_anual])
    add_section("Top herramientas (anual)", [(i.label, i.count) for i in conocimientos.top_herramientas_anual])

    # Mensuales
    add_section("Conocimientos registrados por mes", [(f"Mes {i.month}", i.count) for i in conocimientos.conocimientos_por_mes])
    add_section("Top habilidad blanda por mes", [(f"Mes {i.month}: {i.label}", i.count) for i in conocimientos.top_habilidades_blandas_por_mes])
    add_section("Top habilidad técnica por mes", [(f"Mes {i.month}: {i.label}", i.count) for i in conocimientos.top_habilidades_tecnicas_por_mes])
    add_section("Top herramienta por mes", [(f"Mes {i.month}: {i.label}", i.count) for i in conocimientos.top_herramientas_por_mes])

# ───────────────────────── PREFERENCIAS ──────────────────────
    elements.append(Paragraph("📌 Estadísticas de Preferencias", styles["Heading2"]))

    # Anuales
    add_section("Top disponibilidad de inicio (anual)", [(i.label, i.count) for i in preferencias.top_disponibilidad_inicio_anual])
    add_section("Top rangos salariales (anual)", [(i.label, i.count) for i in preferencias.top_rangos_salariales_anual])
    add_section("Top motivos de salida (anual)", [(i.label, i.count) for i in preferencias.top_motivos_salida_anual])
    add_section("Disponibilidad para viajar (anual)", [(i.label, i.count) for i in preferencias.disponibilidad_viajar_anual])
    add_section("Situación laboral actual (anual)", [(i.label, i.count) for i in preferencias.situacion_laboral_actual_anual])

    # Mensuales
    add_section("Preferencias registradas por mes", [(f"Mes {i.month}", i.count) for i in preferencias.preferencias_por_mes])
    add_section("Top disponibilidad de inicio por mes", [(f"Mes {i.month}: {i.label}", i.count) for i in preferencias.top_disponibilidad_inicio_por_mes])
    add_section("Top rango salarial por mes", [(f"Mes {i.month}: {i.label}", i.count) for i in preferencias.top_rangos_salariales_por_mes])
    add_section("Top motivo de salida por mes", [(f"Mes {i.month}: {i.label}", i.count) for i in preferencias.top_motivos_salida_por_mes])
    add_section("Disponibilidad para viajar por mes", [(f"Mes {i.month}: {i.label}", i.count) for i in preferencias.disponibilidad_viajar_por_mes])
    add_section("Situación laboral actual por mes", [(f"Mes {i.month}: {i.label}", i.count) for i in preferencias.situacion_laboral_actual_por_mes])

    # ───────────────────────── PROCESO ───────────────────────────
    elements.append(Paragraph("📈 Estadísticas del Proceso de Selección", styles["Heading2"]))

    # Anuales
    add_section("Top estados de candidatos (anual)", [(i.label, i.count) for i in proceso.top_estados_anual])

    # Mensuales
    add_section("Candidatos registrados por mes", [(f"Mes {i.month}", i.count) for i in proceso.candidatos_por_mes])
    add_section("Top estado por mes", [(f"Mes {i.month}: {i.label}", i.count) for i in proceso.top_estados_por_mes])


    # Construir y devolver
    doc.build(elements)
    buffer.seek(0)
    return buffer
