from pydantic import BaseModel, Field, field_validator
from pydantic_core import PydanticCustomError
import re
from app.core.security.sanitizador_entrada import SanitizadorDeEntrada
from app.modules.usuarios.schemas.validaciones import UsuarioValidacionConstantes
from app.modules.ubicacion.schemas.validaciones import UbicacionValidacionConstantes

class RegistroPeticion(BaseModel):
    nombre: str = Field(..., max_length=UsuarioValidacionConstantes.NOMBRE_MAX)
    apellidos: str = Field(..., max_length=UsuarioValidacionConstantes.APELLIDOS_MAX)
    correo: str = Field(..., max_length=UsuarioValidacionConstantes.CORREO_MAX)
    clave: str = Field(..., min_length=UsuarioValidacionConstantes.CLAVE_MIN, max_length=UsuarioValidacionConstantes.CLAVE_MAX)
    
    telefono: str = Field(None, max_length=UsuarioValidacionConstantes.TELEFONO_MAX)
    direccion: str = Field(None, max_length=UsuarioValidacionConstantes.DIRECCION_MAX)
    referencia: str = Field(None, max_length=UsuarioValidacionConstantes.REFERENCIA_MAX)
    codigo_postal: str = Field(None, max_length=UsuarioValidacionConstantes.CODIGO_POSTAL_MAX)
    distrito_id: str = Field(None, max_length=UbicacionValidacionConstantes.DISTRITO_ID_MAX)

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

    @field_validator('correo')
    @classmethod
    def validar_correo(cls, v):
        regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if not v or not re.match(regex, v):
            raise PydanticCustomError('value_error', 'El formato del correo electrónico no es válido')
        return v

    @field_validator('clave')
    @classmethod
    def validar_clave(cls, v):
        if not v or len(v) < UsuarioValidacionConstantes.CLAVE_MIN:
            raise PydanticCustomError('value_error', f'La clave debe tener al menos {UsuarioValidacionConstantes.CLAVE_MIN} caracteres')
        return v
