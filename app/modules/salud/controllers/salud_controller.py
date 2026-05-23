from fastapi import APIRouter
from app.core.responses.api_respuesta import ApiDeRespuesta
from app.core.responses.mensajes_confirmacion import MensajesDeConfirmacion
from app.modules.salud.services.salud_mapper import SaludMapper
from app.core.config.sistema_constantes import SistemaConstantes

salud_router = APIRouter()

@salud_router.get('')
async def verificar_salud():
    datos_salud = SaludMapper.de_estado_a_salud_respuesta(
        servicio=SistemaConstantes.NOMBRE_SERVICIO,
        version=SistemaConstantes.VERSION,
        estado=SistemaConstantes.ESTADO_ACTIVO
    )
    return ApiDeRespuesta.exito(
        MensajesDeConfirmacion.DATOS_OBTENIDOS,
        datos_salud
    )
