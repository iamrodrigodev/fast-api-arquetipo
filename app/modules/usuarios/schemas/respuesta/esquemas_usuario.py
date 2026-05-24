from pydantic import BaseModel
from typing import Optional


class RolRespuesta(BaseModel):
    id: int
    nombre: str


class DireccionPerfilRespuesta(BaseModel):
    direccion_exacta: Optional[str] = None
    referencia: Optional[str] = None
    codigo_postal: Optional[str] = None
    distrito_id: Optional[str] = None
    distrito_nombre: Optional[str] = None
    provincia_nombre: Optional[str] = None
    departamento_nombre: Optional[str] = None


class PerfilRespuesta(BaseModel):
    id: int
    nombre: str
    apellidos: str
    correo: str
    telefono: Optional[str] = None
    foto_url: Optional[str] = None
    rol: RolRespuesta
    direccion: Optional[DireccionPerfilRespuesta] = None
