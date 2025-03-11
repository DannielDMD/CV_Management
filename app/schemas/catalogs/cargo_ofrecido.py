from pydantic import BaseModel

class CargoOfrecidoBase(BaseModel):
    nombre_cargo: str
    id_categoria: int

class CargoOfrecidoCreate(CargoOfrecidoBase):
    pass

class CargoOfrecidoResponse(CargoOfrecidoBase):
    id_cargo: int

    class Config:
        from_attributes = True
