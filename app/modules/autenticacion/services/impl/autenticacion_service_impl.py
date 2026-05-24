from datetime import datetime
import hashlib
import logging
from app.modules.usuarios.repositories.usuario_repository import UsuarioRepository
from app.modules.usuarios.repositories.rol_repository import RolRepository
from app.modules.autenticacion.repositories.token_refresco_repository import TokenRefrescoRepository
from app.modules.autenticacion.models.token_refresco import TokenRefresco
from app.modules.usuarios.models.usuario import Usuario
from app.modules.usuarios.models.usuario_direccion import UsuarioDireccion
from app.modules.usuarios.enums.nombre_rol import NombreRol
from app.core.security.servicio_jwt import ServicioJwt
from app.core.security.servicio_hash import ServicioHash
from app.utils.tiempo_util import TiempoUtil
from app.modules.autenticacion.schemas.validaciones import SeguridadValidacionConstantes
from app.core.exceptions.errores_personalizados import ExcepcionDeNegocio, ExcepcionDeRecursoNoEncontrado
from app.core.exceptions.mensajes_error import MensajesDeError
from app.modules.autenticacion.mappers.autenticacion_mapper import AutenticacionMapper
from app.modules.autenticacion.services.autenticacion_service import IAutenticacionService
from app.core.config.ajustes import ajustes

logger = logging.getLogger("fastapi")


class AutenticacionServiceImpl(IAutenticacionService):
    def __init__(self):
        self.usuario_repo = UsuarioRepository()
        self.rol_repo = RolRepository()
        self.token_refresco_repo = TokenRefrescoRepository()
        self.jwt_service = ServicioJwt()
        self.mapper = AutenticacionMapper()

    @staticmethod
    def _hash_token(token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    async def _emitir_tokens_para_usuario(self, usuario):
        token_acceso = self.jwt_service.generar_token_acceso(usuario.id)
        token_refresco = self.jwt_service.generar_token_refresco(usuario.id)

        payload_refresco = self.jwt_service.obtener_payload(token_refresco)
        if not payload_refresco:
            raise ExcepcionDeNegocio(MensajesDeError.ERROR_INTERNO)

        token_entidad = TokenRefresco(
            usuario_id=usuario.id,
            token_hash=self._hash_token(token_refresco),
            expira_en=datetime.fromtimestamp(payload_refresco["exp"]),
        )
        await self.token_refresco_repo.guardar(token_entidad)
        logger.info(f"[AUDITORIA] Emision de tokens para usuario_id={usuario.id}")

        return self.mapper.de_usuario_a_inicio_sesion_respuesta(
            usuario,
            token_acceso,
            token_refresco,
            int(ajustes.jwt_expiracion_token.total_seconds()),
        )

    async def registrar_cuenta(self, datos):
        logger.info(f"Iniciando registro de cuenta para: {datos.correo}")
        if await self.usuario_repo.buscar_por_correo(datos.correo):
            logger.warning(f"Intento de registro con correo duplicado: {datos.correo}")
            raise ExcepcionDeNegocio(MensajesDeError.EMAIL_DUPLICADO)

        rol_usuario = await self.rol_repo.buscar_por_nombre(NombreRol.USUARIO.value)
        if not rol_usuario:
            raise ExcepcionDeRecursoNoEncontrado()

        hashed_pw = ServicioHash.hashear_contrasena(datos.clave)

        nuevo_usuario = Usuario(
            nombre=datos.nombre,
            apellidos=datos.apellidos,
            correo=datos.correo.lower(),
            clave=hashed_pw,
            telefono=datos.telefono,
            rol=rol_usuario,
        )

        if getattr(datos, "direccion", None) or getattr(datos, "distrito_id", None):
            direccion = UsuarioDireccion(
                direccion_exacta=datos.direccion,
                referencia=datos.referencia,
                codigo_postal=datos.codigo_postal,
                distrito_id=datos.distrito_id,
            )
            nuevo_usuario.direccion = direccion

        await self.usuario_repo.guardar(nuevo_usuario)
        logger.info(f"Cuenta registrada exitosamente: {datos.correo}")
        return await self._emitir_tokens_para_usuario(nuevo_usuario)

    async def iniciar_sesion(self, datos):
        logger.info(f"Intento de inicio de sesion: {datos.correo}")
        usuario = await self.usuario_repo.buscar_por_correo(datos.correo.lower())
        if not usuario:
            logger.warning(f"Usuario no encontrado: {datos.correo}")
            raise ExcepcionDeNegocio(MensajesDeError.CREDENCIALES_INVALIDAS)

        ahora = datetime.now()
        await self._validar_bloqueo_login(usuario, ahora)

        if ServicioHash.verificar_contrasena(datos.clave, str(usuario.clave)):
            await self._reiniciar_intentos_login(usuario)
            logger.info(f"Inicio de sesion exitoso: {datos.correo}")
            logger.info(f"[AUDITORIA] Login exitoso usuario_id={usuario.id}")
            return await self._emitir_tokens_para_usuario(usuario)

        logger.warning(f"Credenciales invalidas para: {datos.correo}")
        logger.warning(f"[AUDITORIA] Login fallido correo={datos.correo}")
        await self._registrar_intento_fallido_login(usuario, ahora)
        raise ExcepcionDeNegocio(MensajesDeError.CREDENCIALES_INVALIDAS)

    async def refrescar_token(self, datos):
        payload = self.jwt_service.obtener_payload(datos.token_refresco)
        if not payload or payload.get("tipo") != "refresco":
            logger.warning("[AUDITORIA] Refresh token invalido por payload/tipo")
            raise ExcepcionDeNegocio(MensajesDeError.CREDENCIALES_INVALIDAS)

        token_hash = self._hash_token(datos.token_refresco)
        token_bd = await self.token_refresco_repo.buscar_activo_por_hash(token_hash)
        if not token_bd:
            logger.warning("[AUDITORIA] Intento de reuse o refresh no activo")
            raise ExcepcionDeNegocio(MensajesDeError.CREDENCIALES_INVALIDAS)

        usuario = await self.usuario_repo.buscar_por_id(int(payload["sub"]))
        if not usuario:
            raise ExcepcionDeNegocio(MensajesDeError.USUARIO_NO_ENCONTRADO)

        await self.token_refresco_repo.revocar_por_hash(token_hash)
        logger.info(f"[AUDITORIA] Refresh token rotado usuario_id={usuario.id}")
        return await self._emitir_tokens_para_usuario(usuario)

    async def cerrar_sesion(self, datos):
        token_hash = self._hash_token(datos.token_refresco)
        resultado = await self.token_refresco_repo.revocar_por_hash(token_hash)
        logger.info(f"[AUDITORIA] Cierre de sesion por refresh resultado={resultado}")
        return resultado

    async def cerrar_sesion_todos(self, usuario_id: int) -> int:
        total = await self.token_refresco_repo.revocar_todos_usuario(usuario_id)
        logger.info(f"[AUDITORIA] Cierre de sesion en todos los dispositivos usuario_id={usuario_id} tokens={total}")
        return total

    async def limpiar_tokens_refresco(self) -> int:
        total = await self.token_refresco_repo.limpiar_expirados_y_revocados()
        logger.info(f"[AUDITORIA] Limpieza de tokens_refresco eliminados={total}")
        return total

    async def obtener_sesion(self, usuario):
        return self.mapper.de_usuario_a_inicio_sesion_respuesta(usuario, "", "", 0)

    async def _validar_bloqueo_login(self, usuario, ahora):
        if usuario.fecha_bloqueo_login:
            if TiempoUtil.esta_en_periodo_de_bloqueo(
                ahora, usuario.fecha_bloqueo_login, SeguridadValidacionConstantes.LOGIN_MINUTOS_BLOQUEO
            ):
                minutos = TiempoUtil.calcular_minutos_restantes(
                    ahora, usuario.fecha_bloqueo_login, SeguridadValidacionConstantes.LOGIN_MINUTOS_BLOQUEO
                )
                logger.warning(f"Cuenta bloqueada temporalmente: {usuario.correo}")
                raise ExcepcionDeNegocio(MensajesDeError.CUENTA_BLOQUEADA, detalles=f"Faltan {minutos} minutos")
            usuario.intentos_fallidos_login = 0
            usuario.fecha_bloqueo_login = None
            await self.usuario_repo.guardar(usuario)

    async def _registrar_intento_fallido_login(self, usuario, ahora):
        usuario.intentos_fallidos_login = (usuario.intentos_fallidos_login or 0) + 1
        if usuario.intentos_fallidos_login >= SeguridadValidacionConstantes.LOGIN_MAX_INTENTOS:
            usuario.fecha_bloqueo_login = ahora
            logger.warning(f"Cuenta bloqueada por exceso de intentos: {usuario.correo}")
        await self.usuario_repo.guardar(usuario)

    async def _reiniciar_intentos_login(self, usuario):
        if (usuario.intentos_fallidos_login or 0) > 0:
            usuario.intentos_fallidos_login = 0
            usuario.fecha_bloqueo_login = None
            await self.usuario_repo.guardar(usuario)
