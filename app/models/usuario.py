from sqlalchemy import Column, Integer, String, Boolean
from app.core.database import Base  # importa Base desde donde definas tu motor

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    correo = Column(String(255), unique=True, index=True, nullable=False)
    nombre = Column(String(255))
    rol = Column(String(20), nullable=False, default="TH")  # TH o ADMIN
    activo = Column(Boolean, default=True, nullable=False)
