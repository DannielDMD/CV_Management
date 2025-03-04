from fastapi import FastAPI
from app.core.database import engine
from test import test_db
from fastapi import FastAPI
from app.schemas.candidato import *
from app.schemas.educacion import *
from app.schemas.experiencia import *
from app.schemas.habilidades_blandas import *
from app.schemas.habilidades_tecnicas import *
from app.schemas.herramientas import *
from app.schemas.preferencias import *

app = FastAPI(title="Gestión de Candidatos - Backend")

app.include_router(test_db.router, prefix="/test", tags=["Test"])


""""
PRUEBA DE LA BASE DE DATOS
"""
#Comprobar la conexión a la Base de Datos
@app.get("/check-db")
def check_db():
    try:
        with engine.connect() as connection:
            return {"status": "success", "message": "Conexión con PostgreSQL exitosa 🎉"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    