import jwt
from datetime import datetime, timezone
from src.config.ajustes import ajustes

class ServicioJwt:
    @staticmethod
    def generar_token(usuario_id):
        payload = {
            'sub': str(usuario_id),
            'iat': datetime.now(timezone.utc),
            'exp': datetime.now(timezone.utc) + ajustes.jwt_expiracion_token
        }
        return jwt.encode(
            payload,
            ajustes.JWT_SECRET_KEY,
            algorithm=ajustes.JWT_ALGORITHM
        )

    @staticmethod
    def decodificar_token(token):
        try:
            payload = jwt.decode(
                token,
                ajustes.JWT_SECRET_KEY,
                algorithms=[ajustes.JWT_ALGORITHM]
            )
            return int(payload['sub'])
        except Exception:
            return None
