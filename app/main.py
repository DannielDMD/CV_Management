from fastapi import FastAPI
from app.core.database import engine, Base

# from app.core.config import settings  # Configuración cargada
from fastapi import FastAPI
from app.schemas.candidato import *
from app.schemas.educacion import *
from app.schemas.experiencia import *
from app.schemas.habilidades_blandas import *
from app.schemas.habilidades_tecnicas import *
from app.schemas.herramientas import *
from app.schemas.preferencias import *

# Rutas generales
from app.routes import candidato
from app.routes import educacion
from app.routes import experiencia
from app.routes import habilidades_blandas_candidato
from app.routes import habilidades_tecnicas_candidato
from app.routes import herramientas_candidatos
from app.routes import preferencias

# Rutas de los catalogos
from app.routes.catalogs import (
    ciudades,
    cargos_ofrecidos,
    nivel_educacion,
    titulo,
    instituciones,
    nivel_ingles,
    rangos_experiencia,
)
from app.routes.catalogs import (
    habilidades_blandas,
    habilidades_tecnicas,
    herramientas,
    disponibilidad,
    rangos_salariales,
    motivo_salida,
)

# Imports de rutas de candidato
from app.schemas.catalogs.ciudad import *
from app.schemas.catalogs.cargo_ofrecido import *

# imports de erutas de ducacion
from app.schemas.catalogs.nivel_educacion import *
from app.schemas.catalogs.titulo import *
from app.schemas.catalogs.instituciones import *
from app.schemas.catalogs.nivel_ingles import *

# Imports de rutas de Experiencia
from app.schemas.catalogs.rango_experiencia import *

# Imports de catalogos de Habilidades Blandas
# from app.routes import auth
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Gestión de Candidatos - Backend")
# print(app.routes)

# Incluir rutas
# Rutas de los catalogos
app.include_router(ciudades.router)
# app.include_router (categorias_cargos.router)
app.include_router(cargos_ofrecidos.router)
# Educacion
app.include_router(nivel_educacion.router)
app.include_router(titulo.router)
app.include_router(instituciones.router)
app.include_router(nivel_ingles.router)
# Experiencia
app.include_router(rangos_experiencia.router)
# Habilidades Blandas
app.include_router(habilidades_blandas.router)
# Habilidades Tecnicas
app.include_router(habilidades_tecnicas.router)
# Herramientas
app.include_router(herramientas.router)
# Preferencias
app.include_router(disponibilidad.router)
app.include_router(rangos_salariales.router)
app.include_router(motivo_salida.router)
# Rutas Generales
app.include_router(candidato.router)
app.include_router(educacion.router)
app.include_router(experiencia.router)
app.include_router(habilidades_blandas_candidato.router)
app.include_router(habilidades_tecnicas_candidato.router)
app.include_router(herramientas_candidatos.router)
app.include_router(preferencias.router)


# Cores para el fetch en el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # Permitir cualquier origen. Puedes restringirlo a ['http://127.0.0.1:5500']
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)


# Comprobar la conexión a la Base de Datos
@app.get("/check-db")
def check_db():
    try:
        with engine.connect() as connection:
            return {
                "status": "success",
                "message": "Conexión con PostgreSQL exitosa 🎉",
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}
