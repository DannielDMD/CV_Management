"""Modelo de la tabla 'titulos_obtenidos'."""

from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base

class TituloObtenido(Base):
    """
    Representa los títulos obtenidos por los candidatos, asociados a un nivel educativo.

    Atributos:
        id_titulo (int): Identificador único del título.
        nombre_titulo (str): Nombre del título obtenido.
        id_nivel_educacion (int): Clave foránea al nivel de educación correspondiente.
        nivel_educacion (NivelEducacion): Relación con el nivel de educación asociado.

    Restricciones:
        uq_titulo_nivel: Evita duplicados del mismo título bajo un mismo nivel educativo.
    """
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
