from pydantic import BaseModel

class TituloObtenidoBase(BaseModel):
    nombre_titulo: str
    id_nivel_educacion: int

class TituloObtenidoCreate(TituloObtenidoBase):
    pass

class TituloObtenidoUpdate(BaseModel):
    nombre_titulo: str | None = None
    id_nivel_educacion: int | None = None

class TituloObtenidoResponse(TituloObtenidoBase):
    id_titulo: int

    class Config:
        from_attributes = True
