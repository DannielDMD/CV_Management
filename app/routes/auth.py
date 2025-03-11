"""from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from urllib.parse import urlencode
import httpx
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["Auth"])

# Ruta para redirigir al usuario a Microsoft
@router.get("/login")
async def login():
    params = {
        "client_id": settings.CLIENT_ID,
        "response_type": "code",
        "redirect_uri": settings.REDIRECT_URI,
        "response_mode": "query",
        "scope": "openid profile email User.Read",
    }
    auth_url = f"https://login.microsoftonline.com/{settings.TENANT_ID}/oauth2/v2.0/authorize?" + urlencode(params)
    return RedirectResponse(auth_url)

# Ruta para manejar la respuesta de Microsoft con verificación de `code`
@router.get("/callback")
async def auth_callback(request: Request, code: str = None):
    if not code:
        return {"error": "No code received", "query_params": request.query_params}

    token_url = f"https://login.microsoftonline.com/{settings.TENANT_ID}/oauth2/v2.0/token"

    token_data = {
        "client_id": settings.CLIENT_ID,
        "client_secret": settings.CLIENT_SECRET,
        "code": code,
        "redirect_uri": settings.REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    async with httpx.AsyncClient() as client:
        token_response = await client.post(token_url, data=token_data)
        token_response_json = token_response.json()

        if "error" in token_response_json:
            raise HTTPException(status_code=400, detail=token_response_json)
        
        token = token_response_json.get("access_token")

        if not token:
            raise HTTPException(status_code=400, detail="Token de acceso no recibido")

        # Obtener información del usuario
        headers = {"Authorization": f"Bearer {token}"}
        user_response = await client.get(settings.USER_INFO_URL, headers=headers)
        user_response_json = user_response.json()

        if "error" in user_response_json:
            raise HTTPException(status_code=400, detail=user_response_json)

    return {"user": user_response_json}
"""