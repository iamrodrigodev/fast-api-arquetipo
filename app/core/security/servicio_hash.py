from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")

class ServicioHash:

    @staticmethod
    def hashear_contrasena(clave: str) -> str:
        return pwd_context.hash(clave)

    @staticmethod
    def verificar_contrasena(clave_plana: str, hash_almacenado: str) -> bool:
        return pwd_context.verify(clave_plana, str(hash_almacenado))
