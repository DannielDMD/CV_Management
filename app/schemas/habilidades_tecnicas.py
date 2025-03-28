"""from typing import List, Optional
from pydantic import BaseModel

# Schema para crear una nueva categoría de habilidades técnicas
class CategoriaHabilidadTecnicaCreate(BaseModel):
    nombre_categoria: str

# Schema para representar las categorías de habilidades técnicas
class CategoriaHabilidadTecnicaResponse(BaseModel):
    id_categoria_habilidad: int
    nombre_categoria: str
    
    class Config:
        from_attributes = True

 #Schema para representar una habilidad técnica
class HabilidadTecnicaResponse(BaseModel):
    id_habilidad_tecnica: int
    nombre_habilidad: str
    categoria: CategoriaHabilidadTecnicaResponse

    class Config:
        from_attributes = True
        
# Schema para crear una habilidad técnica
class HabilidadTecnicaCreate(BaseModel):
    nombre_habilidad: str
    id_categoria_habilidad: Optional[int] = None  # Puede ser None si se crea una nueva categoría
    nueva_categoria: Optional[CategoriaHabilidadTecnicaCreate] = None  # Se usa si se quiere crear una categoría nueva


# Schema para actualizar una habilidad técnica
class HabilidadTecnicaUpdate(BaseModel):
    nombre_habilidad: Optional[str] = None
    id_categoria_habilidad: Optional[int] = None

# Schema para asignar una habilidad técnica a un candidato
class HabilidadTecnicaCandidatoCreate(BaseModel):
    id_candidato: int
    id_habilidad_tecnica: int

# Schema para devolver la reEzlación entre candidato y habilidades técnicas
class HabilidadTecnicaCandidatoResponse(BaseModel):
    id: int
    habilidad_tecnica: HabilidadTecnicaResponse
    
    class Config:
        from_attributes = True
"""