"""from pydantic import BaseModel
class EstadoCivilBase(BaseModel):
    nombre_ciudad: str

class EstadoCreate(EstadoCivilBase):
    pass

class EstadoCivilResponse(EstadoCivilBase):
    id_ciudad: int

    class Config:
        from_attributes = True
"""