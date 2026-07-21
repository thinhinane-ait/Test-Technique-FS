##app/core/security.py
##Authentification :** Sécurisez les routes d'écriture (`POST`, `PATCH`)

from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader
from app.core.config import settings


api_key_header = APIKeyHeader(
    name="X-API-key",
    auto_error=False
)
def verify_api_key(
     api_key: str= Security(api_key_header)
     ):
    if api_key != settings.secret_key:
        raise HTTPException(
            status_code=403,
            detail="Clé d'autorisation est invalide"
        )
    return api_key