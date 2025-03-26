from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from sqlalchemy import UniqueConstraint


class TituloObtenido(Base):
    __tablename__ = "titulos_obtenidos"

    id_titulo = Column(Integer, primary_key=True, index=True)
    nombre_titulo = Column(String(100), nullable=False)
    id_nivel_educacion = Column(
        Integer, ForeignKey("nivel_educacion.id_nivel_educacion"), nullable=False
    )

    # Relación con Nivel de Educación
    nivel_educacion = relationship("NivelEducacion", back_populates="titulos")

    __table_args__ = (
        UniqueConstraint("nombre_titulo", "id_nivel_educacion", name="uq_titulo_nivel"),
    )
