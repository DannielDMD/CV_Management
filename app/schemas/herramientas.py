from typing import List
from pydantic import BaseModel

# Schema para representar las categorías de herramientas
class CategoriaHerramientaResponse(BaseModel):
    id_categoria_herramienta: int
    nombre_categoria: str

    class Config:
        from_attributes = True

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
