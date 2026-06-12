from fastapi import APIRouter
from app.core.responses.api_respuesta import ApiDeRespuesta
from app.core.responses.mensajes_confirmacion import MensajesDeConfirmacion
from app.modules.estado.services.estado_mapper import EstadoMapper
from app.core.config.sistema_constantes import SistemaConstantes

estado_router = APIRouter()

@estado_router.get('')
async def verificar_estado():
    datos_estado = EstadoMapper.de_estado_a_estado_respuesta(
        servicio=SistemaConstantes.NOMBRE_SERVICIO,
        version=SistemaConstantes.VERSION,
        estado=SistemaConstantes.ESTADO_ACTIVO
    )
    return ApiDeRespuesta.exito(
        MensajesDeConfirmacion.DATOS_OBTENIDOS,
        datos_estado
    )
