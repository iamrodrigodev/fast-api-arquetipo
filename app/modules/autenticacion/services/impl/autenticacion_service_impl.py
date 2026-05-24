from datetime import datetime, timedelta
import hashlib
import logging
import secrets

from app.modules.usuarios.repositories.usuario_repository import UsuarioRepository
from app.modules.usuarios.repositories.rol_repository import RolRepository
from app.modules.autenticacion.repositories.token_refresco_repository import TokenRefrescoRepository
from app.modules.autenticacion.repositories.seguridad_cuenta_repository import SeguridadCuentaRepository
from app.modules.autenticacion.models.token_refresco import TokenRefresco
from app.modules.autenticacion.models.credencial_usuario import CredencialUsuario
from app.modules.autenticacion.models.estado_login_usuario import EstadoLoginUsuario
from app.modules.autenticacion.models.token_recuperacion_clave import TokenRecuperacionClave
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
        self.seguridad_repo = SeguridadCuentaRepository()
        self.jwt_service = ServicioJwt()
        self.mapper = AutenticacionMapper()

    @staticmethod
    def _hash_token(token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    async def _obtener_o_crear_estado_login(self, usuario_id: int):
        estado = await self.seguridad_repo.obtener_estado_login(usuario_id)
        if not estado:
            estado = EstadoLoginUsuario(usuario_id=usuario_id, intentos_fallidos=0)
            estado = await self.seguridad_repo.guardar_estado_login(estado)
        return estado

    async def _obtener_credencial(self, usuario_id: int):
        credencial = await self.seguridad_repo.obtener_credencial(usuario_id)
        if credencial:
            return credencial
        usuario = await self.usuario_repo.buscar_por_id(usuario_id)
        if not usuario:
            return None
        credencial = CredencialUsuario(usuario_id=usuario_id, hash_clave=usuario.clave)
        return await self.seguridad_repo.guardar_credencial(credencial)

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

        nuevo_usuario = await self.usuario_repo.guardar(nuevo_usuario)
        await self.seguridad_repo.guardar_credencial(CredencialUsuario(usuario_id=nuevo_usuario.id, hash_clave=hashed_pw))
        await self.seguridad_repo.guardar_estado_login(EstadoLoginUsuario(usuario_id=nuevo_usuario.id, intentos_fallidos=0))
        logger.info(f"Cuenta registrada exitosamente: {datos.correo}")
        return await self._emitir_tokens_para_usuario(nuevo_usuario)

    async def iniciar_sesion(self, datos):
        logger.info(f"Intento de inicio de sesion: {datos.correo}")
        usuario = await self.usuario_repo.buscar_por_correo(datos.correo.lower())
        if not usuario:
            logger.warning(f"Usuario no encontrado: {datos.correo}")
            raise ExcepcionDeNegocio(MensajesDeError.CREDENCIALES_INVALIDAS)

        credencial = await self._obtener_credencial(usuario.id)
        if not credencial:
            raise ExcepcionDeNegocio(MensajesDeError.CREDENCIALES_INVALIDAS)

        estado = await self._obtener_o_crear_estado_login(usuario.id)
        ahora = datetime.now()

        if estado.bloqueado_hasta and ahora < estado.bloqueado_hasta:
            minutos = int((estado.bloqueado_hasta - ahora).total_seconds() / 60) + 1
            raise ExcepcionDeNegocio(MensajesDeError.CUENTA_BLOQUEADA, detalles=f"Faltan {minutos} minutos")

        if ServicioHash.verificar_contrasena(datos.clave, str(credencial.hash_clave)):
            estado.intentos_fallidos = 0
            estado.bloqueado_hasta = None
            estado.ultimo_login_ok = ahora
            await self.seguridad_repo.guardar_estado_login(estado)
            logger.info(f"Inicio de sesion exitoso: {datos.correo}")
            logger.info(f"[AUDITORIA] Login exitoso usuario_id={usuario.id}")
            return await self._emitir_tokens_para_usuario(usuario)

        estado.intentos_fallidos = (estado.intentos_fallidos or 0) + 1
        if estado.intentos_fallidos >= SeguridadValidacionConstantes.LOGIN_MAX_INTENTOS:
            estado.bloqueado_hasta = ahora + timedelta(minutes=SeguridadValidacionConstantes.LOGIN_MINUTOS_BLOQUEO)
        await self.seguridad_repo.guardar_estado_login(estado)

        logger.warning(f"Credenciales invalidas para: {datos.correo}")
        logger.warning(f"[AUDITORIA] Login fallido correo={datos.correo}")
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

    async def solicitar_recuperacion_clave(self, datos):
        usuario = await self.usuario_repo.buscar_por_correo(datos.correo.lower())
        if not usuario:
            logger.info(f"[AUDITORIA] Recuperacion solicitada para correo no registrado: {datos.correo}")
            return True

        await self.seguridad_repo.revocar_tokens_recuperacion_usuario(usuario.id)
        token_plano = secrets.token_urlsafe(48)
        token_entidad = TokenRecuperacionClave(
            usuario_id=usuario.id,
            token_hash=self._hash_token(token_plano),
            expira_en=datetime.now() + timedelta(minutes=30),
        )
        await self.seguridad_repo.guardar_token_recuperacion(token_entidad)

        logger.info(f"[AUDITORIA] Recuperacion de clave solicitada usuario_id={usuario.id}")
        logger.info(f"[RECUPERACION_CLAVE_DEV] token_recuperacion={token_plano}")
        return True

    async def restablecer_clave(self, datos):
        token_hash = self._hash_token(datos.token_recuperacion)
        token = await self.seguridad_repo.buscar_token_recuperacion_activo(token_hash)
        if not token:
            logger.warning("[AUDITORIA] Token de recuperacion invalido o expirado")
            raise ExcepcionDeNegocio(MensajesDeError.TOKEN_RECUPERACION_INVALIDO)

        credencial = await self._obtener_credencial(token.usuario_id)
        if not credencial:
            raise ExcepcionDeNegocio(MensajesDeError.USUARIO_NO_ENCONTRADO)

        credencial.hash_clave = ServicioHash.hashear_contrasena(datos.nueva_clave)
        credencial.ultimo_cambio_clave = datetime.now()
        await self.seguridad_repo.guardar_credencial(credencial)
        await self.seguridad_repo.marcar_token_recuperacion_como_usado(token.id)
        await self.token_refresco_repo.revocar_todos_usuario(token.usuario_id)

        logger.info(f"[AUDITORIA] Clave restablecida usuario_id={token.usuario_id}")
        return True

    async def obtener_sesion(self, usuario):
        return self.mapper.de_usuario_a_inicio_sesion_respuesta(usuario, "", "", 0)
