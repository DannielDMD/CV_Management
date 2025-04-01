from pydantic import BaseModel, Field

# Esquema base para HabilidadBlanda
class HabilidadBlandaBase(BaseModel):
    nombre_habilidad_blanda: str = Field(..., title="Nombre de la habilidad blanda", max_length=100)

class HabilidadBlandaCreate(HabilidadBlandaBase):
    pass

class HabilidadBlandaResponse(HabilidadBlandaBase):
    id_habilidad_blanda: int = Field(..., title="ID de la habilidad blanda")

    class Config:
        from_attributes = True


# Esquema base para HabilidadTecnica
class HabilidadTecnicaBase(BaseModel):
    nombre_habilidad_tecnica: str = Field(..., title="Nombre de la habilidad técnica", max_length=100)

class HabilidadTecnicaCreate(HabilidadTecnicaBase):
    pass

class HabilidadTecnicaResponse(HabilidadTecnicaBase):
    id_habilidad_tecnica: int = Field(..., title="ID de la habilidad técnica")

    class Config:
        from_attributes = True


# Esquema base para Herramienta
class HerramientaBase(BaseModel):
    nombre_herramienta: str = Field(..., title="Nombre de la herramienta", max_length=100)

class HerramientaCreate(HerramientaBase):
    pass

class HerramientaResponse(HerramientaBase):
    id_herramienta: int = Field(..., title="ID de la herramienta")

    class Config:
        from_attributes = True
