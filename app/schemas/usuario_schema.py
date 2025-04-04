from pydantic import BaseModel, EmailStr
from typing import Optional


# ✅ Base común (puede compartirse entre creación y edición)
class UsuarioBase(BaseModel):
    correo: EmailStr
    nombre: Optional[str] = None
    rol: str


# ✅ Para crear un nuevo usuario (POST)
class UsuarioCreate(UsuarioBase):
    pass


# ✅ Para exponer un usuario completo (GET)
class UsuarioOut(UsuarioBase):
    id: int
    activo: bool

    class Config:
        orm_mode = True
