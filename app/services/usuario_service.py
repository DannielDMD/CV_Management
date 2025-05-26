from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.schemas import usuario_schema

# ─────────────────────────────────────────────────────────────────────────────
# SERVICIO: Gestión de usuarios del sistema (autorización, listado y registro)
# ─────────────────────────────────────────────────────────────────────────────

def get_usuario_by_correo(db: Session, correo: str):
    """
    Busca un usuario en la base de datos por su correo electrónico.

    Args:
        db (Session): Sesión activa de SQLAlchemy.
        correo (str): Correo electrónico del usuario.

    Returns:
        Usuario | None: Instancia del modelo si existe, de lo contrario None.
    """
    return db.query(Usuario).filter(Usuario.correo == correo).first()


def create_usuario(db: Session, usuario: usuario_schema.UsuarioCreate):
    """
    Crea un nuevo usuario en el sistema.

    Args:
        db (Session): Sesión activa de SQLAlchemy.
        usuario (UsuarioCreate): Datos del usuario a registrar.

    Returns:
        Usuario: Usuario creado y guardado en la base de datos.
    """
    db_usuario = Usuario(
        correo=usuario.correo.lower(),  # normalizamos el correo
        nombre=usuario.nombre,
        rol=usuario.rol,
        activo=True  # se activa por defecto
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


def get_usuarios(db: Session, skip: int = 0, limit: int = 100):
    """
    Devuelve una lista de todos los usuarios registrados en el sistema.

    Args:
        db (Session): Sesión activa de SQLAlchemy.
        skip (int): Número de registros a omitir (paginación).
        limit (int): Límite de registros a retornar.

    Returns:
        list[Usuario]: Lista de usuarios.
    """
    return db.query(Usuario).offset(skip).limit(limit).all()
