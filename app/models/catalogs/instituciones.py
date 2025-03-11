from sqlalchemy import Column, Integer, String
from app.core.database import Base

class InstitucionAcademica(Base):
    __tablename__ = "instituciones_academicas"
    
    id_institucion = Column(Integer, primary_key=True, index=True)
    nombre_institucion = Column(String(150), nullable=False, unique=True)
