"""Ruta para exportar todos los candidatos detallados en archivo Excel."""

from io import BytesIO
from typing import Optional

from fastapi import APIRouter, Depends, Body
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.dashboard.export_service import exportar_candidatos_detallados_excel

router = APIRouter(
    prefix="/reportes",
    tags=["Reportes – Exportación"]
)

class ExportFiltroRequest(BaseModel):
    """
    Modelo de solicitud para aplicar filtro por año al exportar candidatos.

    Atributos:
        año (Optional[int]): Año opcional para filtrar candidatos registrados.
    """
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
    Genera un archivo Excel con la información detallada de todos los candidatos.

    Args:
        filtros (ExportFiltroRequest): Filtro opcional por año de registro.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        StreamingResponse: Archivo Excel como descarga.
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
