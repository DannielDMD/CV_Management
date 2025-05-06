from io import BytesIO
from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from fastapi import Body
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.dashboard.export_service import exportar_candidatos_detallados_excel

router = APIRouter(
    prefix="/reportes",
    tags=["Reportes – Exportación"]
)

class ExportFiltroRequest(BaseModel):
    año: Optional[int] = None

@router.post(
    "/exportar-candidatos",
    summary="Exportar todos los candidatos detallados en un archivo Excel"
)
def exportar_candidatos_excel(
    filtros: ExportFiltroRequest = Body(...),
    db: Session = Depends(get_db)
):
    """
    Genera y devuelve un archivo Excel con la información completa de todos los candidatos.
    Si se envía un año, solo exporta los registrados en ese año.
    """
    output: BytesIO = exportar_candidatos_detallados_excel(db, filtros.año)
    headers = {
        "Content-Disposition": "attachment; filename=candidatos_detallados.xlsx"
    }
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers=headers
    )
