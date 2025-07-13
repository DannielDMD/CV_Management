from jose import jwt
from cachetools import TTLCache
from typing import Dict, Any
import requests
import os

AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID")
AZURE_AUTHORITY = os.getenv("AZURE_AUTHORITY")  # Debe terminar en /v2.0

# URLs para ambas versiones
OPENID_CONFIG_URL_V2 = f"https://login.microsoftonline.com/{AZURE_TENANT_ID}/v2.0/.well-known/openid-configuration"
OPENID_CONFIG_URL_V1 = f"https://login.microsoftonline.com/{AZURE_TENANT_ID}/.well-known/openid-configuration"

jwks_cache = TTLCache(maxsize=2, ttl=60 * 60)  # 1 hora

def get_jwks_uri(version="v2") -> str:
    cache_key = f"jwks_uri_{version}"
    if cache_key in jwks_cache:
        return jwks_cache[cache_key]
    
    config_url = OPENID_CONFIG_URL_V2 if version == "v2" else OPENID_CONFIG_URL_V1
    resp = requests.get(config_url)
    resp.raise_for_status()
    jwks_uri = resp.json()["jwks_uri"]
    jwks_cache[cache_key] = jwks_uri
    return jwks_uri

def get_signing_keys(version="v2") -> Dict[str, Any]:
    jwks_uri = get_jwks_uri(version)
    resp = requests.get(jwks_uri)
    resp.raise_for_status()
    return resp.json()

def validar_token(token: str) -> Dict[str, Any]:
    """Valida un token JWT de Azure y devuelve su payload decodificado."""
    
    # 👇 imprimimos el payload sin validar
    unverified_claims = jwt.get_unverified_claims(token)
    print("🧾 ISSUER del token:", unverified_claims.get("iss"))
    print("🎯 AUDIENCE del token:", unverified_claims.get("aud"))
    print("🔍 VERSION del token:", unverified_claims.get("ver"))
    print("🔍 TOKEN ID:", unverified_claims.get("tid"))
    
    # Determinar versión del token por el issuer
    token_issuer = unverified_claims.get("iss")
    is_v1_token = "sts.windows.net" in token_issuer
    
    # Posibles issuers válidos
    valid_issuers = [
        f"https://sts.windows.net/{AZURE_TENANT_ID}/",  # v1.0
        f"https://login.microsoftonline.com/{AZURE_TENANT_ID}/v2.0"  # v2.0
    ]
    
    # Posibles audiences válidos
    valid_audiences = [
        AZURE_CLIENT_ID,  # Solo el GUID
        f"api://{AZURE_CLIENT_ID}",  # Con prefijo api://
    ]
    
    # Si el CLIENT_ID ya tiene api://, también probamos sin él
    if AZURE_CLIENT_ID.startswith("api://"):
        valid_audiences.append(AZURE_CLIENT_ID.replace("api://", ""))
    
    print(f"🔍 Issuers válidos: {valid_issuers}")
    print(f"🔍 Audiences válidos: {valid_audiences}")
    
    # Obtener claves de firma (v1 y v2 usan las mismas claves)
    try:
        signing_keys = get_signing_keys("v2")
    except:
        signing_keys = get_signing_keys("v1")
    
    headers = jwt.get_unverified_header(token)
    kid = headers.get("kid")
    
    key = next(
        (k for k in signing_keys["keys"] if k["kid"] == kid),
        None,
    )
    
    if not key:
        raise ValueError("Clave de firma no encontrada.")
    
    # Intentar validar con diferentes combinaciones
    last_error = None
    for issuer in valid_issuers:
        for audience in valid_audiences:
            try:
                print(f"🔄 Intentando validar con issuer: {issuer}, audience: {audience}")
                payload = jwt.decode(
                    token,
                    key,
                    algorithms=["RS256"],
                    audience=audience,
                    issuer=issuer,
                )
                print(f"✅ Token válido con issuer: {issuer}, audience: {audience}")
                return payload
            except jwt.JWTError as e:
                print(f"❌ Falló con issuer: {issuer}, audience: {audience} - {str(e)}")
                last_error = e
                continue
    
    # Si llegamos aquí, ninguna combinación funcionó
    raise ValueError(f"Token inválido: {str(last_error)}")
def extraer_correo_token(payload: Dict[str, Any]) -> str:
    """Extrae el correo electrónico del payload del token JWT."""
    # Posibles campos donde puede estar el correo
    campos_correo = [
        "email",
        "preferred_username", 
        "upn",
        "unique_name"
    ]
    
    for campo in campos_correo:
        if campo in payload and payload[campo]:
            return payload[campo]
    
    raise ValueError("No se pudo extraer el correo del token")
def debug_token(token: str) -> Dict[str, Any]:
    """Función para debuggear tokens - útil para desarrollo"""
    try:
        header = jwt.get_unverified_header(token)
        payload = jwt.get_unverified_claims(token)
        
        print("=" * 50)
        print("🔍 DEBUG TOKEN COMPLETO")
        print("=" * 50)
        print(f"HEADER: {header}")
        print(f"PAYLOAD: {payload}")
        print("=" * 50)
        
        return payload
    except Exception as e:
        print(f"❌ Error decodificando token: {e}")
        return {}
    
