"""Módulo principal para levantar la API de Gestión de Candidatos."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
# Jobs
from app.core.database import DATABASE_URL
from app.jobs.limpieza_candidatos import limpiar_candidatos_incompletos_job

# Rutas generales
from app.routes import (
    candidato_route,
    educacion_route,
    experiencia_route,
    conocimientos_candidato_route,
    preferencias_route,
    solicitudes_eliminacion_route,
    usuario_route
)

# Rutas de catálogos
from app.routes.catalogs import (
    centro_costos,
    ciudades,
    cargos_ofrecidos,
    departamentos,
    nivel_educacion,
    titulo,
    instituciones,
    nivel_ingles,
    rangos_experiencia,
    disponibilidad,
    rangos_salariales,
    motivo_salida,
    conocimientos_routes
)

# Rutas de dashboard
from app.routes.Dashboard import (
    stats_general,
    stats_educacion,
    stats_personal,
    stats_experiencia,
    stats_conocimientos,
    stats_preferencias,
    stats_proceso,
    export_report,
    export_pdf
)

# Inicializar aplicación FastAPI
app = FastAPI(title="Gestión de Candidatos - Backend")

# Configuración CORS para permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Puedes usar ["*"] solo para desarrollo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de rutas generales
app.include_router(usuario_route.router)
app.include_router(candidato_route.router)
app.include_router(educacion_route.router)
app.include_router(experiencia_route.router)
app.include_router(conocimientos_candidato_route.router)
app.include_router(preferencias_route.router)
app.include_router(solicitudes_eliminacion_route.router)

# Registro de rutas de catálogos
app.include_router(departamentos.router)
app.include_router(ciudades.router)
app.include_router(cargos_ofrecidos.router)
app.include_router(centro_costos.router)
app.include_router(nivel_educacion.router)
app.include_router(titulo.router)
app.include_router(instituciones.router)
app.include_router(nivel_ingles.router)
app.include_router(rangos_experiencia.router)
app.include_router(conocimientos_routes.router)
app.include_router(disponibilidad.router)
app.include_router(rangos_salariales.router)
app.include_router(motivo_salida.router)

# Registro de rutas del dashboard
app.include_router(stats_general.router)
app.include_router(stats_educacion.router)
app.include_router(stats_personal.router)
app.include_router(stats_experiencia.router)
app.include_router(stats_conocimientos.router)
app.include_router(stats_preferencias.router)
app.include_router(stats_proceso.router)
app.include_router(export_report.router)
app.include_router(export_pdf.router)


print(f"🚀 BASE DE DATOS ACTUAL: {DATABASE_URL}")

# Programación de job periódico para limpiar candidatos incompletos
scheduler = BackgroundScheduler()
scheduler.add_job(limpiar_candidatos_incompletos_job, "interval", hours=6)
scheduler.start()
