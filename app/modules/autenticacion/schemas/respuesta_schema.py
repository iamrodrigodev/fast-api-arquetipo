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
    token: str
