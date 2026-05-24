from pydantic_settings import BaseSettings, SettingsConfigDict
from datetime import timedelta
from pydantic import field_validator

class Ajustes(BaseSettings):
    PUERTO: int = 8000
    CLAVE_SECRETA: str
    ENTORNO: str = "dev"
    CORS_ORIGENES: str = "http://localhost:3000,http://127.0.0.1:3000"
    CORS_CREDENCIALES: bool = True
    DB_FAIL_FAST: bool = True
    LIMPIEZA_TOKENS_HORAS: int = 6
    LIMPIEZA_TOKENS_EN_API: bool = True
    LOG_FORMAT: str = "text"

    DATABASE_URL: str
    
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_EXPIRATION_HOURS: int

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @field_validator("JWT_SECRET_KEY")
    @classmethod
    def validar_jwt_secret(cls, value: str) -> str:
        if len(value) < 32:
            raise ValueError("JWT_SECRET_KEY debe tener al menos 32 caracteres.")
        return value

    @property
    def jwt_expiracion_token(self) -> timedelta:
        return timedelta(hours=self.JWT_EXPIRATION_HOURS)

    @property
    def cors_origenes_lista(self) -> list[str]:
        return [origen.strip() for origen in self.CORS_ORIGENES.split(",") if origen.strip()]

ajustes = Ajustes()
