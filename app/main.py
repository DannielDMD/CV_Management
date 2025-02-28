from fastapi import FastAPI
from app.core.database import engine
from test import test_db


app = FastAPI(title="Gestión de Candidatos - Backend")

app.include_router(test_db.router, prefix="/test", tags=["Test"])

#Comprobar la conexión a la Base de Datos
@app.get("/check-db")
def check_db():
    try:
        with engine.connect() as connection:
            return {"status": "success", "message": "Conexión con PostgreSQL exitosa 🎉"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    