from pydantic_settings import BaseSettings, SettingsConfigDict
from datetime import timedelta

class Ajustes(BaseSettings):
    PUERTO: int = 8000
    CLAVE_SECRETA: str

    DATABASE_URL: str
    
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_EXPIRATION_HOURS: int

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def jwt_expiracion_token(self) -> timedelta:
        return timedelta(hours=self.JWT_EXPIRATION_HOURS)

ajustes = Ajustes()
