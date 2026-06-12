from pydantic_settings import BaseSettings, SettingsConfigDict
from datetime import timedelta
from pydantic import field_validator
from app.core.exceptions.mensajes_error import MensajesDeError

class Ajustes(BaseSettings):
    PUERTO: int
    CLAVE_SECRETA: str
    ENTORNO: str
    CORS_ORIGENES: str
    CORS_CREDENCIALES: bool
    DB_FAIL_FAST: bool
    LIMPIEZA_TOKENS_HORAS: int
    LIMPIEZA_TOKENS_EN_API: bool
    LOG_FORMAT: str

    DATABASE_URL: str
    
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_EXPIRATION_HOURS: int
    JWT_REFRESH_DAYS: int

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @field_validator("JWT_SECRET_KEY")
    @classmethod
    def validar_jwt_secret(cls, value: str) -> str:
        if len(value) < 32:
            raise ValueError(MensajesDeError.JWT_CLAVE_MUY_CORTA.mensaje)
        return value

    @property
    def jwt_expiracion_token(self) -> timedelta:
        return timedelta(hours=self.JWT_EXPIRATION_HOURS)

    @property
    def cors_origenes_lista(self) -> list[str]:
        return [origen.strip() for origen in self.CORS_ORIGENES.split(",") if origen.strip()]

ajustes = Ajustes()
