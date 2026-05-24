from pydantic import BaseModel, Field, field_validator, EmailStr
from pydantic_core import PydanticCustomError
from app.core.security.sanitizador_entrada import SanitizadorDeEntrada
from app.modules.usuarios.schemas.validaciones import UsuarioValidacionConstantes
from app.modules.ubicacion.schemas.validaciones import UbicacionValidacionConstantes


class RegistroPeticion(BaseModel):
    nombre: str = Field(..., max_length=UsuarioValidacionConstantes.NOMBRE_MAX)
    apellidos: str = Field(..., max_length=UsuarioValidacionConstantes.APELLIDOS_MAX)
    correo: EmailStr
    clave: str = Field(..., min_length=UsuarioValidacionConstantes.CLAVE_MIN, max_length=UsuarioValidacionConstantes.CLAVE_MAX)

    telefono: str | None = Field(None, max_length=UsuarioValidacionConstantes.TELEFONO_MAX)
    direccion: str | None = Field(None, max_length=UsuarioValidacionConstantes.DIRECCION_MAX)
    referencia: str | None = Field(None, max_length=UsuarioValidacionConstantes.REFERENCIA_MAX)
    codigo_postal: str | None = Field(None, max_length=UsuarioValidacionConstantes.CODIGO_POSTAL_MAX)
    distrito_id: str | None = Field(None, max_length=UbicacionValidacionConstantes.DISTRITO_ID_MAX)

    @field_validator('nombre', 'apellidos', 'direccion', 'referencia', 'codigo_postal', mode='before')
    @classmethod
    def sanitizar_campos_texto(cls, v):
        if isinstance(v, str):
            return SanitizadorDeEntrada.sanitizar(v)
        return v

    @field_validator('nombre')
    @classmethod
    def validar_nombre(cls, v):
        if not v or len(v.strip()) == 0:
            raise PydanticCustomError('value_error', 'El nombre es obligatorio')
        return v

    @field_validator('apellidos')
    @classmethod
    def validar_apellidos(cls, v):
        if not v or len(v.strip()) == 0:
            raise PydanticCustomError('value_error', 'Los apellidos son obligatorios')
        return v

    @field_validator('correo', mode='before')
    @classmethod
    def sanitizar_correo(cls, v):
        if isinstance(v, str):
            return SanitizadorDeEntrada.sanitizar(v).lower()
        return v

    @field_validator('direccion', 'referencia')
    @classmethod
    def validar_direccion_texto(cls, v):
        if v is not None and len(v.strip()) == 0:
            raise PydanticCustomError('value_error', 'El texto no puede estar vacio')
        return v

    @field_validator('distrito_id')
    @classmethod
    def validar_distrito_id(cls, v):
        if v is not None and len(v.strip()) == 0:
            raise PydanticCustomError('value_error', 'El distrito es obligatorio')
        return v

    @field_validator('clave')
    @classmethod
    def validar_clave(cls, v):
        if not v or len(v) < UsuarioValidacionConstantes.CLAVE_MIN:
            raise PydanticCustomError(
                'value_error',
                'La clave debe tener al menos {min} caracteres',
                {'min': UsuarioValidacionConstantes.CLAVE_MIN}
            )
        return v

    @field_validator('codigo_postal')
    @classmethod
    def validar_codigo_postal(cls, v):
        if v is not None and len(v.strip()) == 0:
            raise PydanticCustomError('value_error', 'El codigo postal no puede estar vacio')
        return v

    @field_validator('telefono')
    @classmethod
    def validar_telefono(cls, v):
        if v is not None and len(v.strip()) == 0:
            raise PydanticCustomError('value_error', 'El telefono no puede estar vacio')
        return v

    @field_validator('distrito_id', mode='after')
    @classmethod
    def validar_coherencia_direccion(cls, distrito_id, info):
        direccion = info.data.get('direccion')
        referencia = info.data.get('referencia')
        if (direccion or referencia) and not distrito_id:
            raise PydanticCustomError('value_error', 'Si envia direccion o referencia, debe enviar distrito_id')
        return distrito_id
