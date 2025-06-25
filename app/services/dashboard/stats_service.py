# app/services/dashboard/stats_service.py

from sqlalchemy.orm import Session
from sqlalchemy import extract, select, distinct
from app.models.candidato_model import Candidato

def obtener_anios_disponibles(db: Session) -> list[int]:
    """
    Obtiene los años únicos donde existen registros de candidatos según fecha_registro.

    Args:
        db (Session): Sesión de base de datos.

    Returns:
        List[int]: Lista de años disponibles con registros.
    """
    query = (
        select(distinct(extract("year", Candidato.fecha_registro)))
        .order_by(extract("year", Candidato.fecha_registro))
    )
    resultados = db.execute(query).scalars().all()
    return [int(a) for a in resultados if a is not None]
