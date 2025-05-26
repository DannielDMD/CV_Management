"""Job programado para eliminar candidatos con formularios incompletos."""

from datetime import datetime, timezone

from app.core.database import SessionLocal
from app.services.candidato_service import eliminar_candidatos_incompletos

def limpiar_candidatos_incompletos_job():
    """
    Tarea programada que elimina periódicamente los candidatos con registros incompletos.

    Utiliza una sesión de base de datos para ejecutar la función correspondiente
    del servicio `eliminar_candidatos_incompletos`, e imprime el número de eliminados
    con marca de tiempo UTC en consola.
    """
    db = SessionLocal()
    try:
        resultado = eliminar_candidatos_incompletos(db)
        print(f"[{datetime.now(timezone.utc)}] Candidatos eliminados: {resultado['eliminados']}")
    finally:
        db.close()
