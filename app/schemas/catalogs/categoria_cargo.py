"""from pydantic import BaseModel

class CategoriaCargoBase(BaseModel):
    nombre_categoria: str

class CategoriaCargoCreate(CategoriaCargoBase):
    pass

class CategoriaCargoResponse(CategoriaCargoBase):
    id_categoria: int

    class Config:
        from_attributes = True
"""