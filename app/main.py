from fastapi import FastAPI
from app.core.database import engine, Base
#from test import test_db
#from app.core.config import settings  # Configuración cargada
from fastapi import FastAPI
from app.schemas.candidato import *
from app.schemas.educacion import *
from app.schemas.experiencia import *
from app.schemas.habilidades_blandas import *
from app.schemas.habilidades_tecnicas import *
from app.schemas.herramientas import *
from app.schemas.preferencias import *
#Rutas generales
from app.routes import candidato
from app.routes import educacion
from app.routes import experiencia
from app.routes import habilidades_blandas
from app.routes import habilidades_tecnicas
from app.routes import herramientas
from app.routes import preferencias
#Rutas de los catalogos
from app.routes.catalogs import categorias_cargos, ciudades, cargos_ofrecidos
#Imports de los catalogos
from app.schemas.catalogs.ciudad import *
from app.schemas.catalogs.cargo_ofrecido import *
from app.schemas.catalogs.categoria_cargo import *
#from app.routes import auth
#from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Gestión de Candidatos - Backend")
#print(app.routes)

# Incluir rutas
#Rutas de los catalogos
app.include_router (ciudades.router)
app.include_router (categorias_cargos.router)
app.include_router (cargos_ofrecidos.router)
#Rutas Generales
app.include_router(candidato.router)
app.include_router (educacion.router)
app.include_router (experiencia.router)
app.include_router (habilidades_blandas.router)
app.include_router (habilidades_tecnicas.router)
app.include_router (herramientas.router)
app.include_router (preferencias.router)


#app.include_router(auth.router)
#PRUEBA DE LA BASE DE DATOS
#Comprobar la conexión a la Base de Datos
@app.get("/check-db")
def check_db():
    try:
        with engine.connect() as connection:
            return {"status": "success", "message": "Conexión con PostgreSQL exitosa 🎉"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    