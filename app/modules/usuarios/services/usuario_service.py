from typing import Protocol
from app.modules.usuarios.schemas.respuesta.esquemas_usuario import PerfilRespuesta
from app.modules.usuarios.models.usuario import Usuario

class IUsuarioService(Protocol):
    async def obtener_perfil(self, usuario: Usuario) -> PerfilRespuesta:
        ...
