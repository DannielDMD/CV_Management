from datetime import datetime, timezone
from app.core.database import SessionLocal
from app.services.candidato_service import eliminar_candidatos_incompletos

def limpiar_candidatos_incompletos_job():
    db = SessionLocal()
    try:
        resultado = eliminar_candidatos_incompletos(db)
        print(f"[{datetime.now(timezone.utc)}] Candidatos eliminados: {resultado['eliminados']}")
    finally:
        db.close()
