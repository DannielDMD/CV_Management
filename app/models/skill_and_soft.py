from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

# 🔹 Modelo para la tabla de Categorías de Habilidades Técnicas
class CategoriaHabilidadTecnica(Base):
    __tablename__ = "categorias_habilidades_tecnicas"

    id_categoria_habilidad = Column(Integer, primary_key=True, index=True)
    nombre_categoria = Column(String(100), nullable=False, unique=True)

    # Relación con Habilidades Técnicas
    habilidades_tecnicas = relationship("HabilidadTecnica", back_populates="categoria")


# 🎯 Modelo para la tabla de Habilidades Técnicas
class HabilidadTecnica(Base):
    __tablename__ = "habilidades_tecnicas"

    id_habilidad_tecnica = Column(Integer, primary_key=True, index=True)
    nombre_habilidad = Column(String(100), nullable=False)
    id_categoria_habilidad = Column(Integer, ForeignKey("categorias_habilidades_tecnicas.id_categoria_habilidad"), nullable=False)

    
    # Relación con Categoría de Habilidades Técnicas
    categoria = relationship("CategoriaHabilidadTecnica", back_populates="habilidades_tecnicas")

    
    # Relación inversa con HabilidadTecnicaCandidato
    candidatos = relationship("HabilidadTecnicaCandidato", back_populates="habilidad_tecnica")
    
    

# 🏅 Modelo para la tabla de Habilidades Técnicas por Candidato
class HabilidadTecnicaCandidato(Base):
    __tablename__ = "habilidades_tecnicas_candidato"

    id = Column(Integer, primary_key=True, index=True)
    id_candidato = Column(Integer, ForeignKey("candidatos.id_candidato"), nullable=False)
    id_habilidad_tecnica = Column(Integer, ForeignKey("habilidades_tecnicas.id_habilidad_tecnica"), nullable=False)

    # Relacion Inversa con Candidatos
    candidato = relationship ("Candidato", back_populates="habilidades_tecnicas")
    
      # Relación con HabilidadTecnica
    habilidad_tecnica = relationship("HabilidadTecnica", back_populates="candidatos")
    

# 🧠 Modelo para la tabla de Habilidades Blandas
class HabilidadBlanda(Base):
    __tablename__ = "habilidades_blandas"

    id_habilidad_blanda = Column(Integer, primary_key=True, index=True)
    nombre_habilidad = Column(String(100), nullable=False, unique=True)

    # Relación con Habilidades Blandas por Candidato
    habilidades_candidatos = relationship("HabilidadBlandaCandidato", back_populates="habilidad_blanda")


# 🤝 Modelo para la tabla de Habilidades Blandas por Candidato
class HabilidadBlandaCandidato(Base):
    __tablename__ = "habilidades_blandas_candidato"

    id = Column(Integer, primary_key=True, index=True)
    id_candidato = Column(Integer, ForeignKey("candidatos.id_candidato"), nullable=False)
    id_habilidad_blanda = Column(Integer, ForeignKey("habilidades_blandas.id_habilidad_blanda"), nullable=False)

    # Relación con Habilidad Blanda
    habilidad_blanda = relationship("HabilidadBlanda", back_populates="habilidades_candidatos")

    # Relacion Inversa con Candidatos
    candidato = relationship ("Candidato", back_populates="habilidades_blandas")  
# 🛠 Modelo para la tabla de Categorías de Herramientas
class CategoriaHerramienta(Base):
    __tablename__ = "categorias_herramientas"

    id_categoria_herramienta = Column(Integer, primary_key=True, index=True)
    nombre_categoria = Column(String(100), nullable=False, unique=True)

    # Relación con Herramientas
    herramientas = relationship("Herramienta", back_populates="categoria")


# 🔧 Modelo para la tabla de Herramientas
class Herramienta(Base):
    __tablename__ = "herramientas"

    id_herramienta = Column(Integer, primary_key=True, index=True)
    nombre_herramienta = Column(String(100), nullable=False)
    id_categoria_herramienta = Column(Integer, ForeignKey("categorias_herramientas.id_categoria_herramienta"), nullable=False)

    # Relación con Categoría de Herramientas
    categoria = relationship("CategoriaHerramienta", back_populates="herramientas")

    # Relación inversa con HerramientaCandidato
    candidatos = relationship("HerramientaCandidato", back_populates="herramienta")

# 🔩 Modelo para la tabla de Herramientas por Candidato (Tabla Intermedia)
class HerramientaCandidato(Base):
    __tablename__ = "herramientas_candidato"

    id = Column(Integer, primary_key=True, index=True)
    id_candidato = Column(Integer, ForeignKey("candidatos.id_candidato"), nullable=False)
    id_herramienta = Column(Integer, ForeignKey("herramientas.id_herramienta"), nullable=False)

    # Relación con Candidato
    candidato = relationship("Candidato", back_populates="herramientas")

    # Relación con Herramienta
    herramienta = relationship("Herramienta", back_populates="candidatos")
