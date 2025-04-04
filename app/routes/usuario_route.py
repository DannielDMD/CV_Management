from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services import usuario_service
from app.schemas import usuario_schema

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


# ✅ Endpoint para crear usuario (admin manual)
@router.post("/", response_model=usuario_schema.UsuarioOut)
def crear_usuario(usuario: usuario_schema.UsuarioCreate, db: Session = Depends(get_db)):
    existente = usuario_service.get_usuario_by_correo(db, usuario.correo)
    if existente:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    return usuario_service.create_usuario(db, usuario)


# ✅ Endpoint para listar usuarios
@router.get("/", response_model=list[usuario_schema.UsuarioOut])
def listar_usuarios(db: Session = Depends(get_db)):
    return usuario_service.get_usuarios(db)


# ✅ Endpoint de autorización (lo usará el frontend)
@router.get("/autorizar/{correo}", response_model=dict)
def autorizar_usuario(correo: str, db: Session = Depends(get_db)):
    usuario = usuario_service.get_usuario_by_correo(db, correo.lower())
    if not usuario or not usuario.activo:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado")

    return {"autorizado": True, "rol": usuario.rol}
