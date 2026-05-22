from fastapi import APIRouter, Depends
from src.service.usuario.impl.usuario_service_impl import UsuarioServiceImpl
from src.response.api_respuesta import ApiDeRespuesta
from src.response.mensajes_confirmacion import MensajesDeConfirmacion
from src.security.configuracion_seguridad import obtener_usuario_actual

usuario_router = APIRouter()
servicio_usuario = UsuarioServiceImpl()

@usuario_router.get('/perfil')
async def obtener_mi_perfil(usuario_actual = Depends(obtener_usuario_actual)):
    return ApiDeRespuesta.exito(
        MensajesDeConfirmacion.DATOS_OBTENIDOS, 
        await servicio_usuario.obtener_perfil(usuario_actual)
    )
