from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

#  Cargar variables de entorno del archivo .env
load_dotenv()

#  Obtener URL de conexión desde .env
DATABASE_URL = os.getenv("DATABASE_URL")

#  Crear motor de la base de datos (engine)
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Mostrar en consola las operaciones SQL (desactiva si no lo necesitas)
    pool_pre_ping=True  # Verifica la conexión antes de usarla (evita errores de desconexión)
)

#  Configuración de sesiones (SessionLocal)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#  Declaración base para los modelos
Base = declarative_base()

#  Dependencia para obtener sesión en cada solicitud de FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#  Probar conexión (opcional)
if __name__ == "__main__":
    try:
        with engine.connect() as connection:
            print("✅ Conexión exitosa a la base de datos 🎉")
    except Exception as e:
        print(f"❌ Error al conectar a la base de datos: {e}")
