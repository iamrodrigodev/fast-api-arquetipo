import logging
import secrets

from app.core.exceptions.errores_personalizados import ExcepcionDeNegocio
from app.core.exceptions.mensajes_error import MensajesDeError
from app.core.security.servicio_hash import ServicioHash
from app.modules.usuarios.mappers.usuario_mapper import UsuarioMapper
from app.modules.usuarios.models.usuario import Usuario
from app.modules.usuarios.repositories.rol_repository import RolRepository
from app.modules.usuarios.repositories.usuario_repository import UsuarioRepository
from app.modules.usuarios.schemas.esquemas_usuario_gestion_peticion import (
    UsuarioGestionActualizarPeticion,
    UsuarioGestionCrearPeticion,
)
from app.modules.usuarios.schemas.respuesta.esquemas_usuario_gestion_respuesta import (
    UsuarioGestionListadoRespuesta,
    UsuarioGestionRespuesta,
)
from app.modules.usuarios.services.usuario_service import IUsuarioService

logger = logging.getLogger("fastapi")


class UsuarioServiceImpl(IUsuarioService):
    def __init__(self):
        self.mapper = UsuarioMapper()
        self.usuario_repo = UsuarioRepository()
        self.rol_repo = RolRepository()

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

    async def crear_usuario_gestion(self, peticion: UsuarioGestionCrearPeticion, administrador_id: int) -> UsuarioGestionRespuesta:
        existente = await self.usuario_repo.buscar_por_correo(peticion.correo)
        if existente:
            raise ExcepcionDeNegocio(MensajesDeError.EMAIL_DUPLICADO)

        rol = await self.rol_repo.buscar_por_id(peticion.rol_id)
        if not rol:
            raise ExcepcionDeNegocio(MensajesDeError.ROL_NO_EXISTE)

        usuario = Usuario(
            nombre=peticion.nombre,
            apellidos=peticion.apellidos,
            correo=peticion.correo,
            clave=ServicioHash.hashear_contrasena(secrets.token_urlsafe(48)),
            telefono=peticion.telefono,
            foto_url=peticion.foto_url,
            rol_id=peticion.rol_id,
            estado=peticion.estado,
        )
        guardado = await self.usuario_repo.guardar(usuario)
        guardado = await self.usuario_repo.buscar_por_id(guardado.id)
        logger.info(f"[AUDITORIA] usuario_creado admin_id={administrador_id} usuario_id={guardado.id}")
        return self.mapper.de_usuario_a_gestion_respuesta(guardado)

    async def listar_usuarios_gestion(self, pagina: int, tamano: int, correo: str | None, rol: int | None, estado: int | None) -> UsuarioGestionListadoRespuesta:
        if pagina < 1:
            raise ExcepcionDeNegocio(MensajesDeError.PAGINACION_INVALIDA)
        if tamano < 1 or tamano > 100:
            raise ExcepcionDeNegocio(MensajesDeError.TAMANO_PAGINA_INVALIDO)
        if estado is not None and estado not in (0, 1):
            raise ExcepcionDeNegocio(MensajesDeError.ESTADO_INVALIDO)

        usuarios, total = await self.usuario_repo.listar_paginado(pagina, tamano, correo, rol, estado)
        items = [self.mapper.de_usuario_a_gestion_respuesta(usuario) for usuario in usuarios]
        return UsuarioGestionListadoRespuesta(items=items, pagina=pagina, tamano=tamano, total=total)

    async def obtener_usuario_gestion(self, usuario_id: int) -> UsuarioGestionRespuesta:
        usuario = await self.usuario_repo.buscar_por_id(usuario_id)
        if not usuario:
            raise ExcepcionDeNegocio(MensajesDeError.USUARIO_NO_ENCONTRADO)
        return self.mapper.de_usuario_a_gestion_respuesta(usuario)

    async def actualizar_usuario_gestion(self, usuario_id: int, peticion: UsuarioGestionActualizarPeticion, administrador_id: int) -> UsuarioGestionRespuesta:
        usuario = await self.usuario_repo.buscar_por_id(usuario_id)
        if not usuario:
            raise ExcepcionDeNegocio(MensajesDeError.USUARIO_NO_ENCONTRADO)

        existente = await self.usuario_repo.buscar_por_correo(peticion.correo)
        if existente and int(existente.id) != int(usuario_id):
            raise ExcepcionDeNegocio(MensajesDeError.EMAIL_DUPLICADO)

        rol = await self.rol_repo.buscar_por_id(peticion.rol_id)
        if not rol:
            raise ExcepcionDeNegocio(MensajesDeError.ROL_NO_EXISTE)

        if int(administrador_id) == int(usuario_id) and peticion.estado == 0:
            raise ExcepcionDeNegocio(MensajesDeError.NO_PUEDE_AUTODESACTIVARSE)

        usuario.nombre = peticion.nombre
        usuario.apellidos = peticion.apellidos
        usuario.correo = peticion.correo
        usuario.telefono = peticion.telefono
        usuario.foto_url = peticion.foto_url
        usuario.rol_id = peticion.rol_id
        usuario.estado = peticion.estado

        guardado = await self.usuario_repo.guardar(usuario)
        guardado = await self.usuario_repo.buscar_por_id(guardado.id)
        logger.info(f"[AUDITORIA] usuario_actualizado admin_id={administrador_id} usuario_id={guardado.id}")
        return self.mapper.de_usuario_a_gestion_respuesta(guardado)

    async def cambiar_estado_usuario_gestion(self, usuario_id: int, estado: int, administrador_id: int) -> UsuarioGestionRespuesta:
        usuario = await self.usuario_repo.buscar_por_id(usuario_id)
        if not usuario:
            raise ExcepcionDeNegocio(MensajesDeError.USUARIO_NO_ENCONTRADO)

        if int(administrador_id) == int(usuario_id) and estado == 0:
            raise ExcepcionDeNegocio(MensajesDeError.NO_PUEDE_AUTODESACTIVARSE)

        usuario.estado = estado
        guardado = await self.usuario_repo.guardar(usuario)
        guardado = await self.usuario_repo.buscar_por_id(guardado.id)
        logger.info(f"[AUDITORIA] usuario_estado_cambiado admin_id={administrador_id} usuario_id={guardado.id} estado={estado}")
        return self.mapper.de_usuario_a_gestion_respuesta(guardado)

    async def eliminar_logico_usuario_gestion(self, usuario_id: int, administrador_id: int) -> None:
        _ = await self.cambiar_estado_usuario_gestion(usuario_id, 0, administrador_id)
        logger.info(f"[AUDITORIA] usuario_baja_logica admin_id={administrador_id} usuario_id={usuario_id}")
