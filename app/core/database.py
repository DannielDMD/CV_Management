"""Configuración de la base de datos para el proyecto Gestión de Candidatos."""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# URL de conexión a la base de datos (PostgreSQL)
DATABASE_URL = os.getenv("DATABASE_URL")

# Motor de conexión a la base de datos
engine = create_engine(
    DATABASE_URL,
    echo=True,           # Muestra las sentencias SQL en consola (útil en desarrollo)
    pool_pre_ping=True   # Verifica conexión antes de usarla
)

# Configuración de sesiones de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa para los modelos
Base = declarative_base()

def get_db():
    """
    Generador de sesión de base de datos para inyectar en rutas o servicios.

    Yields:
        Session: sesión activa de SQLAlchemy.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
