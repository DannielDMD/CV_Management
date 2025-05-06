# routes/Dashboard/export_report.py

from io import BytesIO
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.dashboard.export_service import exportar_candidatos_detallados_excel

router = APIRouter(
    prefix="/reportes",
    tags=["Reportes – Exportación"]
)

@router.post(
    "/exportar-candidatos",
    summary="Exportar todos los candidatos detallados en un archivo Excel"
)
def exportar_candidatos_excel(db: Session = Depends(get_db)):
    """
    Genera y devuelve un archivo Excel con la información completa de todos los candidatos.
    """
    output: BytesIO = exportar_candidatos_detallados_excel(db)
    headers = {
        "Content-Disposition": "attachment; filename=candidatos_detallados.xlsx"
    }
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers=headers
    )
