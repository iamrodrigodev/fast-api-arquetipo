import bcrypt
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError

hasher_argon2 = PasswordHasher()

class ServicioHash:

    @staticmethod
    def hashear_contrasena(clave: str) -> str:
        return hasher_argon2.hash(clave)

    @staticmethod
    def verificar_contrasena(clave_plana: str, hash_almacenado: str) -> bool:
        hash_str = str(hash_almacenado)
        if hash_str.startswith("$argon2"):
            try:
                return hasher_argon2.verify(hash_str, clave_plana)
            except VerifyMismatchError:
                return False
            except InvalidHashError:
                return False
        try:
            if hash_str.startswith("$2a$") or hash_str.startswith("$2b$") or hash_str.startswith("$2y$"):
                return bcrypt.checkpw(clave_plana.encode("utf-8"), hash_str.encode("utf-8"))
            return False
        except (ValueError, TypeError):
            return False
