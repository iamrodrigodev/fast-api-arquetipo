from pydantic import BaseModel
from typing import Optional


class RolRespuesta(BaseModel):
    id: int
    nombre: str


class InicioSesionRespuesta(BaseModel):
    id: int
    nombre: str
    rol: RolRespuesta
    token_acceso: str
    token_refresco: str
    tipo_token: str = "Bearer"
    expira_en_segundos: int
