from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.security.servicio_jwt import ServicioJwt
from app.modules.usuarios.repositories.usuario_repository import UsuarioRepository
from app.modules.usuarios.enums.nombre_rol import NombreRol


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/autenticacion/iniciar-sesion")


async def obtener_usuario_actual(token: str = Depends(oauth2_scheme)):
    usuario_id = ServicioJwt.decodificar_token(token)
    if not usuario_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Fallo en la autenticacion, intente nuevamente",
            headers={"WWW-Authenticate": "Bearer"},
        )

    usuario = await UsuarioRepository.buscar_por_id(usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if getattr(usuario, "estado", 1) != 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario inactivo",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return usuario


def requiere_rol(rol_nombre: str):
    def verificador_rol(usuario=Depends(obtener_usuario_actual)):
        if usuario.rol.nombre != rol_nombre:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acceso denegado: no tiene los permisos necesarios",
            )
        return usuario

    return verificador_rol


def verificar_propietario_o_admin(usuario_objetivo_id: int, usuario_actual) -> None:
    es_admin = usuario_actual.rol and usuario_actual.rol.nombre == NombreRol.ADMINISTRADOR.value
    es_propietario = int(usuario_actual.id) == int(usuario_objetivo_id)
    if not (es_admin or es_propietario):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado: no puede acceder a recursos de otro usuario",
        )
