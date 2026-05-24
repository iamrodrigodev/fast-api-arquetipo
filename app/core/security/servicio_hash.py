from passlib.context import CryptContext
from passlib.exc import UnknownHashError
import bcrypt

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

class ServicioHash:

    @staticmethod
    def hashear_contrasena(clave: str) -> str:
        return pwd_context.hash(clave)

    @staticmethod
    def verificar_contrasena(clave_plana: str, hash_almacenado: str) -> bool:
        hash_str = str(hash_almacenado)
        try:
            return pwd_context.verify(clave_plana, hash_str)
        except (ValueError, TypeError, UnknownHashError):
            # Fallback para hashes legacy bcrypt ante incompatibilidades passlib/bcrypt
            if hash_str.startswith("$2a$") or hash_str.startswith("$2b$") or hash_str.startswith("$2y$"):
                return bcrypt.checkpw(clave_plana.encode("utf-8"), hash_str.encode("utf-8"))
            raise
