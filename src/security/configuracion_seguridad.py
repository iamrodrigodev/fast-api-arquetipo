from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.security.servicio_jwt import ServicioJwt
from src.repository.usuario_repository import UsuarioRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/autenticacion/login")

async def obtener_usuario_actual(token: str = Depends(oauth2_scheme)):
    usuario_id = ServicioJwt.decodificar_token(token)
    if not usuario_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Fallo en la autenticación, intente nuevamente",
            headers={"WWW-Authenticate": "Bearer"},
        )
    usuario = await UsuarioRepository.buscar_por_id(usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return usuario

def requiere_rol(rol_nombre: str):
    def verificador_rol(usuario = Depends(obtener_usuario_actual)):
        # Asume que usuario.rol se cargó de forma "eager" o se permite acceder
        if usuario.rol.nombre != rol_nombre:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acceso Denegado: No tiene los permisos necesarios"
            )
        return usuario
    return verificador_rol
