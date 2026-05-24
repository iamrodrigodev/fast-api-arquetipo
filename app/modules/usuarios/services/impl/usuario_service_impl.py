import logging
from app.modules.usuarios.mappers.usuario_mapper import UsuarioMapper
from app.core.exceptions.errores_personalizados import ExcepcionDeNegocio
from app.core.exceptions.mensajes_error import MensajesDeError
from app.modules.usuarios.services.usuario_service import IUsuarioService
from app.modules.usuarios.repositories.usuario_repository import UsuarioRepository

logger = logging.getLogger("fastapi")

class UsuarioServiceImpl(IUsuarioService):
    def __init__(self):
        self.mapper = UsuarioMapper()
        self.usuario_repo = UsuarioRepository()

    async def obtener_perfil(self, usuario):
        if not usuario:
            raise ExcepcionDeNegocio(MensajesDeError.USUARIO_NO_ENCONTRADO)
            
        logger.info(f"Obteniendo perfil para el usuario: {usuario.correo}")
        return self.mapper.de_usuario_a_perfil_respuesta(usuario)

    async def obtener_perfil_por_id(self, usuario_id: int):
        usuario = await self.usuario_repo.buscar_por_id(usuario_id)
        if not usuario:
            raise ExcepcionDeNegocio(MensajesDeError.USUARIO_NO_ENCONTRADO)
        return self.mapper.de_usuario_a_perfil_respuesta(usuario)
