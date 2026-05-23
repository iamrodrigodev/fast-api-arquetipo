from pydantic import BaseModel
from typing import Optional

class RolRespuesta(BaseModel):
    id: int
    nombre: str

class PerfilRespuesta(BaseModel):
    id: int
    nombre: str
    apellidos: str
    correo: str
    telefono: Optional[str] = None
    foto_url: Optional[str] = None
    rol: RolRespuesta
