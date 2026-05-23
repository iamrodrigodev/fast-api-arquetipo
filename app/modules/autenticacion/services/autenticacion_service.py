import bcrypt
from datetime import datetime, timezone
import logging
from app.modules.usuarios.repositories.usuario_repository import UsuarioRepository
from app.modules.usuarios.repositories.rol_repository import RolRepository
from app.modules.usuarios.models.usuario import Usuario
from app.modules.usuarios.models.usuario_direccion import UsuarioDireccion
from app.modules.usuarios.models.rol import NombreRol
from app.core.security.servicio_jwt import ServicioJwt
from app.utils.tiempo_util import TiempoUtil
from app.modules.autenticacion.schemas.validaciones import SeguridadValidacionConstantes
from app.core.exceptions.errores_personalizados import ExcepcionDeNegocio, ExcepcionDeRecursoNoEncontrado
from app.core.exceptions.mensajes_error import MensajesDeError
from app.modules.autenticacion.services.autenticacion_mapper import AutenticacionMapper
from app.modules.autenticacion.services.autenticacion_service import IAutenticacionService

logger = logging.getLogger("fastapi")

class AutenticacionServiceImpl(IAutenticacionService):
    def __init__(self):
        self.usuario_repo = UsuarioRepository()
        self.rol_repo = RolRepository()
        self.jwt_service = ServicioJwt()
        self.mapper = AutenticacionMapper()

    async def registrar_cuenta(self, datos):
        logger.info(f"Iniciando registro de cuenta para: {datos.correo}")
        if await self.usuario_repo.buscar_por_correo(datos.correo):
            logger.warning(f"Intento de registro con correo duplicado: {datos.correo}")
            raise ExcepcionDeNegocio(MensajesDeError.EMAIL_DUPLICADO)

        rol_usuario = await self.rol_repo.buscar_por_nombre(NombreRol.USUARIO.value)
        if not rol_usuario:
            raise ExcepcionDeRecursoNoEncontrado()

        hashed_pw = bcrypt.hashpw(datos.clave.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        nuevo_usuario = Usuario(
            nombre=datos.nombre,
            apellidos=datos.apellidos,
            correo=datos.correo.lower(),
            clave=hashed_pw,
            telefono=datos.telefono,
            rol=rol_usuario
        )

        if getattr(datos, 'direccion', None) or getattr(datos, 'distrito_id', None):
            direccion = UsuarioDireccion(
                direccion_exacta=datos.direccion,
                referencia=datos.referencia,
                codigo_postal=datos.codigo_postal,
                distrito_id=datos.distrito_id
            )
            nuevo_usuario.direccion = direccion

        await self.usuario_repo.guardar(nuevo_usuario)
        logger.info(f"Cuenta registrada exitosamente: {datos.correo}")
        return None

    async def iniciar_sesion(self, datos):
        logger.info(f"Intento de inicio de sesión: {datos.correo}")
        usuario = await self.usuario_repo.buscar_por_correo(datos.correo.lower())
        if not usuario:
            logger.warning(f"Usuario no encontrado: {datos.correo}")
            raise ExcepcionDeNegocio(MensajesDeError.CREDENCIALES_INVALIDAS)

        ahora = datetime.now(timezone.utc)
        await self._validar_bloqueo_login(usuario, ahora)

        if bcrypt.checkpw(datos.clave.encode('utf-8'), usuario.clave.encode('utf-8')):
            token = self.jwt_service.generar_token(usuario.id)
            await self._reiniciar_intentos_login(usuario)
            logger.info(f"Inicio de sesión exitoso: {datos.correo}")
            return self.mapper.de_usuario_a_inicio_sesion_respuesta(usuario, token)
        else:
            logger.warning(f"Credenciales inválidas para: {datos.correo}")
            await self._registrar_intento_fallido_login(usuario, ahora)
            raise ExcepcionDeNegocio(MensajesDeError.CREDENCIALES_INVALIDAS)

    async def obtener_sesion(self, usuario):
        return self.mapper.de_usuario_a_inicio_sesion_respuesta(usuario, "")

    async def _validar_bloqueo_login(self, usuario, ahora):
        if usuario.fecha_bloqueo_login:
            if TiempoUtil.esta_en_periodo_de_bloqueo(ahora, usuario.fecha_bloqueo_login, SeguridadValidacionConstantes.LOGIN_MINUTOS_BLOQUEO):
                minutos = TiempoUtil.calcular_minutos_restantes(ahora, usuario.fecha_bloqueo_login, SeguridadValidacionConstantes.LOGIN_MINUTOS_BLOQUEO)
                logger.warning(f"Cuenta bloqueada temporalmente: {usuario.correo}")
                raise ExcepcionDeNegocio(MensajesDeError.CUENTA_BLOQUEADA, detalles=f"Faltan {minutos} minutos")
            else:
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
        if usuario.intentos_fallidos_login > 0:
            usuario.intentos_fallidos_login = 0
            usuario.fecha_bloqueo_login = None
            await self.usuario_repo.guardar(usuario)
