from fastapi import APIRouter, Depends
from app.modules.usuarios.services.usuario_service import IUsuarioService
from app.core.responses.api_respuesta import ApiDeRespuesta
from app.core.responses.mensajes_confirmacion import MensajesDeConfirmacion
from app.core.security.seguridad import obtener_usuario_actual
from app.core.dependencies.dependencias import get_usuario_service

usuario_router = APIRouter()

@usuario_router.get('/perfil')
async def obtener_mi_perfil(
    usuario_actual = Depends(obtener_usuario_actual),
    servicio_usuario: IUsuarioService = Depends(get_usuario_service)
):
    respuesta = await servicio_usuario.obtener_perfil(usuario_actual)
    return ApiDeRespuesta.exito(MensajesDeConfirmacion.DATOS_OBTENIDOS, respuesta.model_dump())
