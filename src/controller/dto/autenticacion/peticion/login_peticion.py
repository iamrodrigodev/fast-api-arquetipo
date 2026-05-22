from pydantic import BaseModel, Field, field_validator
from pydantic_core import PydanticCustomError
from src.security.sanitizacion.sanitizador_entrada import SanitizadorDeEntrada

class LoginPeticion(BaseModel):
    correo: str = Field(...)
    clave: str = Field(...)

    @field_validator('correo', mode='before')
    @classmethod
    def sanitizar_correo(cls, v):
        if isinstance(v, str):
            return SanitizadorDeEntrada.sanitizar(v)
        return v

    @field_validator('correo')
    @classmethod
    def validar_correo(cls, v):
        if not v or len(v.strip()) == 0:
            raise PydanticCustomError('value_error', 'El correo electrónico es obligatorio')
        return v

    @field_validator('clave')
    @classmethod
    def validar_clave(cls, v):
        if not v or len(v.strip()) == 0:
            raise PydanticCustomError('value_error', 'La clave es obligatoria')
        return v
