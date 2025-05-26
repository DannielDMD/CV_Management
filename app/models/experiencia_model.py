"""Modelo de la tabla 'experiencia_laboral'."""

from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class ExperienciaLaboral(Base):
    """
    Representa un registro de experiencia laboral de un candidato.

    Atributos:
        id_experiencia (int): Identificador único de la experiencia.
        id_candidato (int): Clave foránea al candidato.
        id_rango_experiencia (int): Clave foránea al rango de experiencia total.
        ultima_empresa (str): Nombre de la empresa donde trabajó por última vez.
        ultimo_cargo (str): Último cargo ocupado por el candidato.
        funciones (str): Descripción de las funciones desempeñadas.
        fecha_inicio (date): Fecha de inicio del trabajo.
        fecha_fin (date): Fecha de finalización (puede ser nula si continúa trabajando).

    Relaciones:
        rango_experiencia (RangoExperiencia): Rango de duración de la experiencia.
        candidato (Candidato): Candidato asociado al registro.
    """
    __tablename__ = "experiencia_laboral"

    id_experiencia = Column(Integer, primary_key=True, index=True)
    id_candidato = Column(
        Integer, ForeignKey("candidatos.id_candidato"), nullable=False
    )
    id_rango_experiencia = Column(
        Integer, ForeignKey("rangos_experiencia.id_rango_experiencia"), nullable=False
    )
    ultima_empresa = Column(String(150), nullable=False)
    ultimo_cargo = Column(String(100), nullable=False)
    funciones = Column(Text, nullable=True)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=True)

    # Relaciones
    rango_experiencia = relationship("RangoExperiencia", back_populates="experiencias")
    candidato = relationship("Candidato", back_populates="experiencias")
