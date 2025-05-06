from pydantic import BaseModel


class EstadisticasCandidatosResponse(BaseModel):
    total: int
    EN_PROCESO: int = 0
    ENTREVISTA: int = 0
    ADMITIDO: int = 0
    DESCARTADO: int = 0
    CONTRATADO: int = 0

    class Config:
        from_attributes = True  # Para mantenerlo igual que el resto
