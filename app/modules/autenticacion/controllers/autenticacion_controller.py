from fastapi import APIRouter
from app.modules.autenticacion.schemas.registro_schema import RegistroPeticion
from app.modules.autenticacion.schemas.login_schema import LoginPeticion
from app.modules.autenticacion.services.autenticacion_service import AutenticacionServiceImpl
from app.core.responses.api_respuesta import ApiDeRespuesta
from app.core.responses.mensajes_confirmacion import MensajesDeConfirmacion

autenticacion_router = APIRouter()
servicio_auth = AutenticacionServiceImpl()

@autenticacion_router.post('/registrar-cuenta', status_code=201)
async def registrar_cuenta(peticion: RegistroPeticion):
    return ApiDeRespuesta.creado(MensajesDeConfirmacion.CUENTA_REGISTRADA, await servicio_auth.registrar_cuenta(peticion))

@autenticacion_router.post('/iniciar-sesion')
async def iniciar_sesion(peticion: LoginPeticion):
    return ApiDeRespuesta.exito(MensajesDeConfirmacion.LOGIN_EXITOSO, await servicio_auth.iniciar_sesion(peticion))

@autenticacion_router.post('/cerrar-sesion')
async def cerrar_sesion():
    return ApiDeRespuesta.exito(MensajesDeConfirmacion.SESION_CERRADA)
