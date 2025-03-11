from pydantic import BaseModel

class CiudadBase(BaseModel):
    nombre_ciudad: str

class CiudadCreate(CiudadBase):
    pass

class CiudadResponse(CiudadBase):
    id_ciudad: int

    class Config:
        from_attributes = True
