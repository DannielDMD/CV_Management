from typing import List, Optional
from pydantic import BaseModel

# Schema para crear una categoría de herramientas
class CategoriaHerramientaCreate(BaseModel):
    nombre_categoria: str

# Schema para actualizar una categoría de herramientas
class CategoriaHerramientaUpdate(BaseModel):
    nombre_categoria: Optional[str]

# Schema para representar las categorías de herramientas
class CategoriaHerramientaResponse(BaseModel):
    id_categoria_herramienta: int
    nombre_categoria: str

    class Config:
        from_attributes = True

# Schema para crear una herramienta
class HerramientaCreate(BaseModel):
    nombre_herramienta: str
    id_categoria_herramienta: int

# Schema para actualizar una herramienta
class HerramientaUpdate(BaseModel):
    nombre_herramienta: Optional[str]
    id_categoria_herramienta: Optional[int]

# Schema para representar las herramientas
class HerramientaResponse(BaseModel):
    id_herramienta: int
    nombre_herramienta: str
    categoria: CategoriaHerramientaResponse

    class Config:
        from_attributes = True

# Schema para asignar una herramienta a un candidato
class HerramientaCandidatoCreate(BaseModel):
    id_candidato: int
    id_herramienta: int

# Schema para devolver la relación entre candidato y herramientas
class HerramientaCandidatoResponse(BaseModel):
    id: int
    herramienta: HerramientaResponse

    class Config:
        from_attributes = True
