from fastapi import APIRouter, Depends
from app.modules.usuarios.services.usuario_service import UsuarioServiceImpl
from app.core.responses.api_respuesta import ApiDeRespuesta
from app.core.responses.mensajes_confirmacion import MensajesDeConfirmacion
from app.core.security.seguridad import obtener_usuario_actual

usuario_router = APIRouter()
servicio_usuario = UsuarioServiceImpl()

@usuario_router.get('/perfil')
async def obtener_mi_perfil(usuario_actual = Depends(obtener_usuario_actual)):
    return ApiDeRespuesta.exito(
        MensajesDeConfirmacion.DATOS_OBTENIDOS, 
        await servicio_usuario.obtener_perfil(usuario_actual)
    )
