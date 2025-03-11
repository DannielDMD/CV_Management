"""from dotenv import load_dotenv
import os


load_dotenv()

class Settings:
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    TENANT_ID = os.getenv("TENANT_ID")
    REDIRECT_URI = os.getenv("REDIRECT_URI")
    AUTHORITY = os.getenv("AUTHORITY")
    TOKEN_URL = os.getenv("TOKEN_URL")
    USER_INFO_URL = os.getenv("USER_INFO_URL")

    # Validar que no falten valores críticos
    required_vars = ["CLIENT_ID", "CLIENT_SECRET", "TENANT_ID", "REDIRECT_URI", "TOKEN_URL", "USER_INFO_URL"]
    for var in required_vars:
        if not locals()[var]:
            raise ValueError(f"Error: {var} no está configurado en el .env")

settings = Settings()"""