"""Configuración de la base de datos para el proyecto Gestión de Candidatos."""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Solo cargar .env si estás en desarrollo local
if os.getenv("ENV") != "production":
    from dotenv import load_dotenv
    load_dotenv()

# URL de conexión a la base de datos (PostgreSQL)
DATABASE_URL = os.getenv("DATABASE_URL")

# Motor de conexión a la base de datos
engine = create_engine(
    DATABASE_URL,
    echo=os.getenv("ENV") != "production",  # Mostrar SQL solo en desarrollo
    pool_pre_ping=True
)

# Configuración de sesiones de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa para los modelos
Base = declarative_base()

def get_db():
    """Generador de sesión de base de datos para inyectar en rutas o servicios."""
    print(f"📡 Conectado a: {DATABASE_URL}") 
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
