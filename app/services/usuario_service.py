from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.schemas import usuario_schema


# ✅ Consultar por correo (para validación de acceso)
def get_usuario_by_correo(db: Session, correo: str):
    return db.query(Usuario).filter(Usuario.correo == correo).first()


# ✅ Crear nuevo usuario
def create_usuario(db: Session, usuario: usuario_schema.UsuarioCreate):
    db_usuario = Usuario(
        correo=usuario.correo.lower(),  # normalizamos
        nombre=usuario.nombre,
        rol=usuario.rol,
        activo=True
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


# ✅ Listar todos los usuarios (útil para futura vista de admin)
def get_usuarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Usuario).offset(skip).limit(limit).all()
