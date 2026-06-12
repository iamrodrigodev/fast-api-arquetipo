from datetime import datetime

from pydantic import BaseModel

from app.modules.usuarios.schemas.respuesta.esquemas_usuario import RolRespuesta


class UsuarioGestionRespuesta(BaseModel):
    id: int
    nombre: str
    apellidos: str
    correo: str
    telefono: str | None = None
    foto_url: str | None = None
    estado: int
    rol: RolRespuesta
    fecha_creacion: datetime | None = None
    fecha_actualizacion: datetime | None = None


class UsuarioGestionListadoRespuesta(BaseModel):
    items: list[UsuarioGestionRespuesta]
    pagina: int
    tamano: int
    total: int
