from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.models.educacion_model import Educacion
from app.models.catalogs.nivel_educacion import NivelEducacion

router = APIRouter(prefix="/dashboard/stats", tags=["Estadísticas Educación"])

@router.get("/educacion")
def get_educational_distribution(db: Session = Depends(get_db)):
    resultados = (
        db.query(NivelEducacion.descripcion_nivel, func.count(Educacion.id_educacion).label("total"))
        .join(Educacion, Educacion.id_nivel_educacion == NivelEducacion.id_nivel_educacion)
        .group_by(NivelEducacion.descripcion_nivel)
        .order_by(func.count(Educacion.id_educacion).desc())
        .all()
    )

    return [{"nivel": descripcion, "total": total} for descripcion, total in resultados]
