from pydantic import BaseModel

class NivelInglesResponse(BaseModel):
    id_nivel_ingles: int
    nivel: str

    class Config:
        from_attributes = True

class NivelInglesCreate(BaseModel):
    nivel: str

class NivelInglesUpdate(BaseModel):
    nivel: str
