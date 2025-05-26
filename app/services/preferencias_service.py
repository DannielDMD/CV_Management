from sqlalchemy.orm import Session
from app.models.preferencias import PreferenciaDisponibilidad
from app.schemas.preferencias_schema import PreferenciaDisponibilidadCreate, PreferenciaDisponibilidadUpdate, PreferenciaDisponibilidadResponse
from app.utils.orden_catalogos import ordenar_por_nombre

# ──────────────────────────────────────────────────────────────────────────────
# SERVICIO: Preferencias de disponibilidad del candidato
# Este módulo gestiona la lógica CRUD de las preferencias laborales (disponibilidad,
# salario, razones para trabajar en Joyco, etc.) asociadas a un candidato.
# ──────────────────────────────────────────────────────────────────────────────

def obtener_preferencia_candidato(db: Session, id_candidato: int):
    """
    Retorna la preferencia de disponibilidad asociada a un candidato específico.

    Args:
        db (Session): Sesión de base de datos.
        id_candidato (int): ID del candidato.

    Returns:
        PreferenciaDisponibilidad | None: Registro encontrado o None si no existe.
    """
    return db.query(PreferenciaDisponibilidad).filter(
        PreferenciaDisponibilidad.id_candidato == id_candidato
    ).first()


def crear_preferencia(db: Session, preferencia_data: PreferenciaDisponibilidadCreate):
    """
    Crea una nueva preferencia de disponibilidad para un candidato.

    Args:
        db (Session): Sesión de base de datos.
        preferencia_data (PreferenciaDisponibilidadCreate): Datos del formulario.

    Returns:
        PreferenciaDisponibilidad: Objeto recién creado y persistido.
    """
    nueva_preferencia = PreferenciaDisponibilidad(**preferencia_data.dict())
    db.add(nueva_preferencia)
    db.commit()
    db.refresh(nueva_preferencia)
    return nueva_preferencia


def actualizar_preferencia(db: Session, id_candidato: int, preferencia_data: PreferenciaDisponibilidadUpdate):
    """
    Actualiza los datos de preferencia de disponibilidad para un candidato.

    Args:
        db (Session): Sesión de base de datos.
        id_candidato (int): ID del candidato.
        preferencia_data (PreferenciaDisponibilidadUpdate): Campos a actualizar.

    Returns:
        PreferenciaDisponibilidad | None: Registro actualizado o None si no existe.
    """
    preferencia = obtener_preferencia_candidato(db, id_candidato)
    if not preferencia:
        return None

    for key, value in preferencia_data.dict(exclude_unset=True).items():
        setattr(preferencia, key, value)

    db.commit()
    db.refresh(preferencia)
    return preferencia


def eliminar_preferencia(db: Session, id_candidato: int):
    """
    Elimina el registro de preferencias del candidato dado.

    Args:
        db (Session): Sesión de base de datos.
        id_candidato (int): ID del candidato.

    Returns:
        bool: True si fue eliminado, False si no se encontró.
    """
    preferencia = obtener_preferencia_candidato(db, id_candidato)
    if not preferencia:
        return None

    db.delete(preferencia)
    db.commit()
    return True
