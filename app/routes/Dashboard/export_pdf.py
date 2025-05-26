"""Ruta para exportar estadísticas en formato PDF utilizando ReportLab."""

from io import BytesIO
from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.database import get_db
from app.services.dashboard.export_pdf_service import exportar_estadisticas_pdf_reportlab

router = APIRouter(
    prefix="/reportes",
    tags=["Reportes – Exportación PDF"]
)

class PDFExportRequest(BaseModel):
    """
    Modelo de solicitud para exportar estadísticas en PDF.

    Atributos:
        año (Optional[int]): Año opcional para filtrar las estadísticas.
    """
    año: Optional[int] = None


@router.post(
    "/exportar-estadisticas-pdf",
    summary="Generar y descargar todas las estadísticas en PDF (ReportLab)"
)
def exportar_estadisticas_pdf_endpoint(
    request: PDFExportRequest,
    db: Session = Depends(get_db)
):
    """
    Genera un informe PDF con todas las estadísticas del sistema.

    Incluye:
      - Información personal
      - Educación
      - Experiencia laboral
      - Conocimientos
      - Preferencias y disponibilidad
      - Proceso de selección

    Args:
        request (PDFExportRequest): Filtro opcional por año.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        StreamingResponse: PDF generado como archivo descargable.
    """
    pdf_io: BytesIO = exportar_estadisticas_pdf_reportlab(db, año=request.año)
    headers = {
        "Content-Disposition": "attachment; filename=estadisticas_report.pdf"
    }
    return StreamingResponse(
        pdf_io,
        media_type="application/pdf",
        headers=headers
    )
