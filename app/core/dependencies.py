from fastapi import Header, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import Optional

from app.core.azure_auth import validar_token, extraer_correo_token
from app.core.database import get_db
from app.services.usuario_service import get_usuario_by_correo
from app.models.usuario import Usuario

async def obtener_usuario_actual(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> Usuario:
    """
    Verifica el token, valida al usuario en base de datos y lo retorna.
    """
    
    if not authorization or not authorization.startswith("Bearer "):
        print("❌ Token no proporcionado o malformado")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autorización no proporcionado o inválido.",
        )
    
    token = authorization.replace("Bearer ", "").strip()
    print(f"🔒 Token recibido: {token[:40]}...")  # Mostramos parte del token
    
    try:
        payload = validar_token(token)
        print("✅ Token válido. Payload decodificado:")
        print(payload)
        
        # Usar la nueva función para extraer el correo
        correo = extraer_correo_token(payload)
        print(f"📧 Correo extraído del token: {correo}")
        
        if not correo:
            print("❌ No se pudo extraer el correo del token")
            print(f"🔍 Campos disponibles en el token: {list(payload.keys())}")
            raise ValueError("No se pudo extraer el correo del token.")
            
    except ValueError as e:
        print(f"❌ Token inválido: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token inválido: {str(e)}",
        )
    
    usuario = get_usuario_by_correo(db, correo.lower())
    print(f"🔍 Usuario encontrado en base de datos: {usuario}")
    
    if not usuario or not usuario.activo:
        print("🚫 Usuario no autorizado o inactivo.")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario no autorizado o inactivo.",
        )
    
    print("✅ Usuario autorizado. Retornando objeto Usuario.")
    return usuario