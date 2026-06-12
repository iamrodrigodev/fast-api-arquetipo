from pydantic import BaseModel, EmailStr, Field, field_validator

from app.modules.usuarios.schemas.validaciones import UsuarioValidacionConstantes


class UsuarioGestionCrearPeticion(BaseModel):
    nombre: str = Field(min_length=1, max_length=UsuarioValidacionConstantes.NOMBRE_MAX)
    apellidos: str = Field(min_length=1, max_length=UsuarioValidacionConstantes.APELLIDOS_MAX)
    correo: EmailStr
    telefono: str | None = Field(default=None, max_length=UsuarioValidacionConstantes.TELEFONO_MAX)
    foto_url: str | None = Field(default=None, max_length=UsuarioValidacionConstantes.FOTO_URL_MAX)
    rol_id: int
    estado: int = Field(default=1)

    @field_validator('nombre', 'apellidos')
    @classmethod
    def validar_texto(cls, value: str) -> str:
        texto = value.strip()
        if not texto:
            raise ValueError('Este campo es obligatorio')
        return texto

    @field_validator('estado')
    @classmethod
    def validar_estado(cls, value: int) -> int:
        if value not in (0, 1):
            raise ValueError('El estado debe ser 0 o 1')
        return value


class UsuarioGestionActualizarPeticion(BaseModel):
    nombre: str = Field(min_length=1, max_length=UsuarioValidacionConstantes.NOMBRE_MAX)
    apellidos: str = Field(min_length=1, max_length=UsuarioValidacionConstantes.APELLIDOS_MAX)
    correo: EmailStr
    telefono: str | None = Field(default=None, max_length=UsuarioValidacionConstantes.TELEFONO_MAX)
    foto_url: str | None = Field(default=None, max_length=UsuarioValidacionConstantes.FOTO_URL_MAX)
    rol_id: int
    estado: int = Field(default=1)

    @field_validator('nombre', 'apellidos')
    @classmethod
    def validar_texto(cls, value: str) -> str:
        texto = value.strip()
        if not texto:
            raise ValueError('Este campo es obligatorio')
        return texto

    @field_validator('estado')
    @classmethod
    def validar_estado(cls, value: int) -> int:
        if value not in (0, 1):
            raise ValueError('El estado debe ser 0 o 1')
        return value


class UsuarioGestionEstadoPeticion(BaseModel):
    estado: int

    @field_validator('estado')
    @classmethod
    def validar_estado(cls, value: int) -> int:
        if value not in (0, 1):
            raise ValueError('El estado debe ser 0 o 1')
        return value
