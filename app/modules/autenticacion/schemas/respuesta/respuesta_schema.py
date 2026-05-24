from pydantic import BaseModel
from typing import Optional


class RolRespuesta(BaseModel):
    id: int
    nombre: str


class InicioSesionRespuesta(BaseModel):
    id: int
    nombre: str
    apellidos: str
    correo: str
    foto_url: Optional[str] = None
    rol: RolRespuesta
    token_acceso: str
    token_refresco: str
    tipo_token: str = "Bearer"
    expira_en_segundos: int
