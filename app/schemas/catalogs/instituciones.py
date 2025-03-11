from pydantic import BaseModel

class InstitucionAcademicaBase(BaseModel):
    nombre_institucion: str

class InstitucionAcademicaCreate(InstitucionAcademicaBase):
    pass

class InstitucionAcademicaUpdate(BaseModel):
    nombre_institucion: str | None = None

class InstitucionAcademicaResponse(InstitucionAcademicaBase):
    id_institucion: int

    class Config:
        from_attributes = True
