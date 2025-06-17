"""Rutas para la gestión de usuarios en el sistema."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services import usuario_service
from app.schemas import usuario_schema

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.post("/", response_model=usuario_schema.UsuarioOut)
def crear_usuario(usuario: usuario_schema.UsuarioCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo usuario manualmente (uso interno).

    Args:
        usuario (UsuarioCreate): Datos del nuevo usuario.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        UsuarioOut: Usuario creado.

    Raises:
        HTTPException: Si el correo ya está registrado.
    """
    existente = usuario_service.get_usuario_by_correo(db, usuario.correo)
    if existente:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    return usuario_service.create_usuario(db, usuario)

@router.get("/{id}", response_model=usuario_schema.UsuarioOut)
def obtener_usuario(id: int, db: Session = Depends(get_db)):
    usuario = usuario_service.get_usuario_by_id(db, id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.put("/{id}", response_model=usuario_schema.UsuarioOut)
def actualizar_usuario(id: int, data: usuario_schema.UsuarioUpdate, db: Session = Depends(get_db)):
    actualizado = usuario_service.update_usuario(db, id, data)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado o no se pudo actualizar")
    return actualizado

@router.get("/", response_model=list[usuario_schema.UsuarioOut])
def listar_usuarios(db: Session = Depends(get_db)):
    """
    Lista todos los usuarios registrados.

    Args:
        db (Session): Sesión de base de datos inyectada.

    Returns:
        List[UsuarioOut]: Lista de usuarios.
    """
    return usuario_service.get_usuarios(db)


@router.get("/autorizar/{correo}", response_model=dict)
def autorizar_usuario(correo: str, db: Session = Depends(get_db)):
    """
    Verifica si un usuario está autorizado para acceder (según su correo).

    Args:
        correo (str): Correo del usuario.
        db (Session): Sesión de base de datos inyectada.

    Returns:
        dict: { autorizado: True, rol: str }

    Raises:
        HTTPException: Si el usuario no existe o no está activo.
    """
    usuario = usuario_service.get_usuario_by_correo(db, correo.lower())
    if not usuario or not usuario.activo:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado")

    return {"autorizado": True, "rol": usuario.rol}

@router.delete("/{id}", response_model=dict)
def eliminar_usuario(id: int, db: Session = Depends(get_db)):
    eliminado = usuario_service.delete_usuario(db, id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado o no se pudo eliminar")
    return {"mensaje": "Usuario eliminado exitosamente"}