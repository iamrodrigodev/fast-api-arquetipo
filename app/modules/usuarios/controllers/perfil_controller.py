from fastapi import APIRouter, Depends

from app.core.dependencies.dependencias import get_usuario_service
from app.core.responses.api_respuesta import ApiDeRespuesta
from app.core.responses.mensajes_confirmacion import MensajesDeConfirmacion
from app.core.security.seguridad import (
    obtener_usuario_actual,
    verificador_propietario_o_admin_dep,
)
from app.modules.usuarios.services.usuario_service import IUsuarioService

perfil_router = APIRouter()


@perfil_router.get('/perfil')
async def obtener_mi_perfil(
    usuario_actual=Depends(obtener_usuario_actual),
    servicio_usuario: IUsuarioService = Depends(get_usuario_service)
):
    respuesta = await servicio_usuario.obtener_perfil(usuario_actual)
    return ApiDeRespuesta.exito(MensajesDeConfirmacion.DATOS_OBTENIDOS, respuesta.model_dump())


@perfil_router.get('/{usuario_id}/perfil', dependencies=[Depends(verificador_propietario_o_admin_dep)])
async def obtener_perfil_por_usuario_id(
    usuario_id: int,
    servicio_usuario: IUsuarioService = Depends(get_usuario_service)
):
    respuesta = await servicio_usuario.obtener_perfil_por_id(usuario_id)
    return ApiDeRespuesta.exito(MensajesDeConfirmacion.DATOS_OBTENIDOS, respuesta.model_dump())
