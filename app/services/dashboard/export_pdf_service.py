from io import BytesIO
from datetime import datetime
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

def exportar_estadisticas_pdf_reportlab(db: Session) -> BytesIO:
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
    personal = obtener_estadisticas_personales(db)
    educacion = obtener_estadisticas_educacion(db)
    experiencia = obtener_estadisticas_experiencia(db)
    conocimientos = obtener_estadisticas_conocimientos(db)
    preferencias = obtener_estadisticas_preferencias(db)
    proceso = obtener_estadisticas_proceso(db)

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
    elements.append(Spacer(1, 24))

    def add_section(title, data_rows):
        elements.append(Paragraph(title, styles["Heading2"]))
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

    # Agregar cada sección
    add_section(
        "Información Personal",
        [(item.label, item.count) for item in personal.top_ciudades],
    )
    add_section(
        "Educación",
        [(item.label, item.count) for item in educacion.top_niveles_educacion],
    )
    add_section(
        "Experiencia",
        [(item.label, item.count) for item in experiencia.top_rangos_experiencia],
    )
    add_section(
        "Conocimientos Blandas",
        [(item.label, item.count) for item in conocimientos.top_habilidades_blandas],
    )
    add_section(
        "Preferencias Disponibilidad",
        [(item.label, item.count) for item in preferencias.disponibilidad_inicio],
    )

    # Sección Proceso
    elements.append(Paragraph("Proceso de Selección", styles["Heading2"]))
    proc_rows = [(estado, cant) for estado, cant in proceso.items() if estado != "total"]
    table_proc = Table([["Estado", "Cantidad"]] + proc_rows, colWidths=[300, 100])
    table_proc.setStyle(
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
    elements.append(table_proc)

    # Construir PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer
