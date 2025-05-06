from fastapi import FastAPI
from app.core.database import engine, Base

# from app.core.config import settings  # Configuración cargada
from fastapi import FastAPI

# Schemas
from app.schemas.candidato_schema import *
from app.schemas.educacion_schema import *
from app.schemas.experiencia_schema import *
from app.schemas.preferencias_schema import *

# Rutas generales
from app.routes import candidato_route
from app.routes import educacion_route
from app.routes import experiencia_route
from app.routes import conocimientos_candidato_route
from app.routes import preferencias_route

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
    disponibilidad,
    rangos_salariales,
    motivo_salida,
    conocimientos_routes,
)

# Imports de rutas de candidato
from app.schemas.catalogs.ciudad import *
from app.schemas.catalogs.cargo_ofrecido import *

# imports de erutas de educacion
from app.schemas.catalogs.nivel_educacion import *
from app.schemas.catalogs.titulo import *
from app.schemas.catalogs.instituciones import *
from app.schemas.catalogs.nivel_ingles import *

# Imports de rutas de Experiencia
from app.schemas.catalogs.rango_experiencia import *

# from app.routes import auth
from fastapi.middleware.cors import CORSMiddleware

# from app.routes.Dashboard import dashboard_routes

from app.routes.Dashboard import stats_general, stats_personal

from app.routes.Dashboard import stats_educacion


from apscheduler.schedulers.background import BackgroundScheduler
from app.jobs.limpieza_candidatos import limpiar_candidatos_incompletos_job





print(engine.url)


app = FastAPI(title="Gestión de Candidatos - Backend")

# Cores para el fetch en el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Puedes usar ["*"] solo para desarrollo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(dashboard_routes.router)

from app.routes import usuario_route

app.include_router(usuario_route.router)


app.include_router(stats_general.router)

app.include_router(stats_educacion.router)

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
# Rutas de Conocimientos
app.include_router(conocimientos_routes.router)
# Preferencias
app.include_router(disponibilidad.router)
app.include_router(rangos_salariales.router)
app.include_router(motivo_salida.router)
# Rutas Generales
app.include_router(candidato_route.router)
app.include_router(educacion_route.router)
app.include_router(experiencia_route.router)
app.include_router(conocimientos_candidato_route.router)
app.include_router(preferencias_route.router)

app.include_router (stats_personal.router)



# Crear scheduler y agregar job cada 6 horas
scheduler = BackgroundScheduler()
scheduler.add_job(limpiar_candidatos_incompletos_job, "interval", hours=6)
scheduler.start()



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
