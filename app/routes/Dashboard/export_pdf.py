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
    Genera un PDF con:
      - Estadísticas de Información Personal
      - Educación
      - Experiencia
      - Conocimientos
      - Preferencias
      - Proceso
    usando ReportLab, y lo devuelve como descarga.
    Opcionalmente se puede filtrar por año.
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
