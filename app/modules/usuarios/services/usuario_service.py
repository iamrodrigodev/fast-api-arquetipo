from typing import Protocol

from app.modules.usuarios.models.usuario import Usuario
from app.modules.usuarios.schemas.esquemas_usuario_gestion_peticion import (
    UsuarioGestionActualizarPeticion,
    UsuarioGestionCrearPeticion,
)
from app.modules.usuarios.schemas.respuesta.esquemas_usuario import PerfilRespuesta
from app.modules.usuarios.schemas.respuesta.esquemas_usuario_gestion_respuesta import (
    UsuarioGestionListadoRespuesta,
    UsuarioGestionRespuesta,
)


class IUsuarioService(Protocol):
    async def obtener_perfil(self, usuario: Usuario) -> PerfilRespuesta:
        ...

    async def obtener_perfil_por_id(self, usuario_id: int) -> PerfilRespuesta:
        ...

    async def crear_usuario_gestion(self, peticion: UsuarioGestionCrearPeticion, administrador_id: int) -> UsuarioGestionRespuesta:
        ...

    async def listar_usuarios_gestion(self, pagina: int, tamano: int, correo: str | None, rol: int | None, estado: int | None) -> UsuarioGestionListadoRespuesta:
        ...

    async def obtener_usuario_gestion(self, usuario_id: int) -> UsuarioGestionRespuesta:
        ...

    async def actualizar_usuario_gestion(self, usuario_id: int, peticion: UsuarioGestionActualizarPeticion, administrador_id: int) -> UsuarioGestionRespuesta:
        ...

    async def cambiar_estado_usuario_gestion(self, usuario_id: int, estado: int, administrador_id: int) -> UsuarioGestionRespuesta:
        ...

    async def eliminar_logico_usuario_gestion(self, usuario_id: int, administrador_id: int) -> None:
        ...
