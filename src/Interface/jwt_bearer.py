from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import DecodeError, ExpiredSignatureError

from src.Interface.init_app import jwt_service


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        credentials: HTTPAuthorizationCredentials | None = await super(JWTBearer, self).__call__(request)
        if not credentials:
            raise HTTPException(status_code=403, detail="Code d'autorisation invalide.")

        if not credentials.scheme == "Bearer":
            raise HTTPException(status_code=403, detail="Schéma d'authentification invalide.")

        token = credentials.credentials

        # Vérification : le jeton est-il dans la liste noire ?
        if token in jwt_service.blacklist:
            raise HTTPException(status_code=403, detail="Jeton invalidé (blacklisté).")

        # Validation du jeton
        try:
            jwt_service.validate_user_jwt(credentials.credentials)
        except ExpiredSignatureError as e:
            raise HTTPException(status_code=403, detail="Jeton expiré.") from e
        except DecodeError as e:
            raise HTTPException(status_code=403, detail="Erreur lors du décodage du jeton.") from e
        except Exception as e:
            raise HTTPException(status_code=403, detail="Erreur inconnue.") from e

        return credentials
