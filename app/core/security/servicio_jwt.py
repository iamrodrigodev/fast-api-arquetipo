import jwt
from datetime import datetime, timezone, timedelta
from uuid import uuid4
from jwt import InvalidTokenError, ExpiredSignatureError, InvalidSignatureError, DecodeError
from app.core.config.ajustes import ajustes


class ServicioJwt:
    @staticmethod
    def generar_token_acceso(usuario_id):
        payload = {
            "sub": str(usuario_id),
            "tipo": "acceso",
            "jti": str(uuid4()),
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + ajustes.jwt_expiracion_token,
        }
        return jwt.encode(payload, ajustes.JWT_SECRET_KEY, algorithm=ajustes.JWT_ALGORITHM)

    @staticmethod
    def generar_token_refresco(usuario_id):
        payload = {
            "sub": str(usuario_id),
            "tipo": "refresco",
            "jti": str(uuid4()),
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(days=7),
        }
        return jwt.encode(payload, ajustes.JWT_SECRET_KEY, algorithm=ajustes.JWT_ALGORITHM)

    @staticmethod
    def decodificar_token(token):
        try:
            payload = jwt.decode(token, ajustes.JWT_SECRET_KEY, algorithms=[ajustes.JWT_ALGORITHM])
            return int(payload["sub"])
        except (ExpiredSignatureError, InvalidSignatureError, DecodeError, InvalidTokenError, KeyError, ValueError, TypeError):
            return None

    @staticmethod
    def obtener_payload(token):
        try:
            return jwt.decode(token, ajustes.JWT_SECRET_KEY, algorithms=[ajustes.JWT_ALGORITHM])
        except (ExpiredSignatureError, InvalidSignatureError, DecodeError, InvalidTokenError, KeyError, ValueError, TypeError):
            return None
