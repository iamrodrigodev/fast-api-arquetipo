from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from app.core.security.servicio_jwt import ServicioJwt
from app.modules.usuarios.repositories.usuario_repository import UsuarioRepository
from app.core.exceptions.errores_personalizados import ExcepcionDeNegocio
from app.core.exceptions.mensajes_error import MensajesDeError
from app.modules.usuarios.enums.roles_sistema import RolesSistema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/autenticacion/iniciar-sesion")


async def obtener_usuario_actual(token: str = Depends(oauth2_scheme)):
    usuario_id = ServicioJwt.decodificar_token(token)
    if not usuario_id:
        raise ExcepcionDeNegocio(MensajesDeError.FALLO_AUTENTICACION)

    usuario = await UsuarioRepository.buscar_por_id(usuario_id)
    if not usuario:
        raise ExcepcionDeNegocio(MensajesDeError.CREDENCIALES_INVALIDAS)

    if getattr(usuario, "estado", 1) != 1:
        raise ExcepcionDeNegocio(MensajesDeError.USUARIO_INACTIVO)

    return usuario


async def obtener_usuario_actual_id(usuario_actual=Depends(obtener_usuario_actual)) -> int:
    return int(usuario_actual.id)


def requiere_rol(rol_nombre: str):
    def verificador_rol(usuario=Depends(obtener_usuario_actual)):
        if usuario.rol.nombre != rol_nombre:
            raise ExcepcionDeNegocio(MensajesDeError.SIN_PERMISOS)
        return usuario

    return verificador_rol


def verificar_propietario_o_admin(usuario_objetivo_id: int, usuario_actual) -> None:
    es_admin = usuario_actual.rol and usuario_actual.rol.nombre == RolesSistema.ADMINISTRADOR.value
    es_propietario = int(usuario_actual.id) == int(usuario_objetivo_id)
    if not (es_admin or es_propietario):
        raise ExcepcionDeNegocio(MensajesDeError.RECURSO_AJENO)


def verificador_propietario_o_admin_dep(usuario_id: int, usuario_actual=Depends(obtener_usuario_actual)):
    verificar_propietario_o_admin(usuario_id, usuario_actual)
    return usuario_actual


def verificar_propietario(usuario_objetivo_id: int, usuario_actual) -> None:
    if int(usuario_actual.id) != int(usuario_objetivo_id):
        raise ExcepcionDeNegocio(MensajesDeError.RECURSO_AJENO)

from fastapi import Header

async def obtener_usuario_actual_opcional(authorization: str | None = Header(default=None)):
    if not authorization or not authorization.startswith('Bearer '):
        return None
    token = authorization.split(' ', 1)[1].strip()
    usuario_id = ServicioJwt.decodificar_token(token)
    if not usuario_id:
        return None
    usuario = await UsuarioRepository.buscar_por_id(usuario_id)
    if not usuario or getattr(usuario, 'estado', 1) != 1:
        return None
    return usuario

