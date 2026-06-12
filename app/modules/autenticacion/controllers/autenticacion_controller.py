from fastapi import APIRouter, Depends
from app.core.dependencies.dependencias import get_autenticacion_service
from app.core.security.seguridad import obtener_usuario_actual_id
from app.core.responses.api_respuesta import ApiDeRespuesta
from app.core.responses.mensajes_confirmacion import MensajesDeConfirmacion
from app.core.security.rate_limit import (
    dep_rate_limit_login,
    dep_rate_limit_recuperacion,
    dep_rate_limit_refresh,
)
from app.modules.autenticacion.schemas.peticion.login_schema import LoginPeticion
from app.modules.autenticacion.schemas.peticion.recuperacion_clave_schema import (
    RestablecerClavePeticion,
    SolicitarRecuperacionClavePeticion,
)
from app.modules.autenticacion.schemas.peticion.refrescar_token_schema import RefrescarTokenPeticion
from app.modules.autenticacion.schemas.peticion.registro_schema import RegistroPeticion
from app.modules.autenticacion.services.autenticacion_service import IAutenticacionService


autenticacion_router = APIRouter()


@autenticacion_router.post('/registrar-cuenta', status_code=201)
async def registrar_cuenta(
    peticion: RegistroPeticion,
    servicio_auth: IAutenticacionService = Depends(get_autenticacion_service)
):
    respuesta = await servicio_auth.registrar_cuenta(peticion)
    return ApiDeRespuesta.creado(MensajesDeConfirmacion.CUENTA_REGISTRADA, respuesta.model_dump())


@autenticacion_router.post('/iniciar-sesion', dependencies=[Depends(dep_rate_limit_login)])
async def iniciar_sesion(
    peticion: LoginPeticion,
    servicio_auth: IAutenticacionService = Depends(get_autenticacion_service)
):
    respuesta = await servicio_auth.iniciar_sesion(peticion)
    return ApiDeRespuesta.exito(MensajesDeConfirmacion.LOGIN_EXITOSO, respuesta.model_dump())


@autenticacion_router.post('/refrescar-token', dependencies=[Depends(dep_rate_limit_refresh)])
async def refrescar_token(
    peticion: RefrescarTokenPeticion,
    servicio_auth: IAutenticacionService = Depends(get_autenticacion_service)
):
    respuesta = await servicio_auth.refrescar_token(peticion)
    return ApiDeRespuesta.exito(MensajesDeConfirmacion.DATOS_OBTENIDOS, respuesta.model_dump())


@autenticacion_router.post('/cerrar-sesion')
async def cerrar_sesion(
    peticion: RefrescarTokenPeticion,
    servicio_auth: IAutenticacionService = Depends(get_autenticacion_service)
):
    await servicio_auth.cerrar_sesion(peticion)
    return ApiDeRespuesta.exito(MensajesDeConfirmacion.SESION_CERRADA)


@autenticacion_router.post('/cerrar-sesion-todos')
async def cerrar_sesion_todos(
    usuario_actual_id: int = Depends(obtener_usuario_actual_id),
    servicio_auth: IAutenticacionService = Depends(get_autenticacion_service)
):
    await servicio_auth.cerrar_sesion_todos(usuario_actual_id)
    return ApiDeRespuesta.exito(MensajesDeConfirmacion.SESION_CERRADA)


@autenticacion_router.post('/solicitar-recuperacion-clave', dependencies=[Depends(dep_rate_limit_recuperacion)])
async def solicitar_recuperacion_clave(
    peticion: SolicitarRecuperacionClavePeticion,
    servicio_auth: IAutenticacionService = Depends(get_autenticacion_service)
):
    await servicio_auth.solicitar_recuperacion_clave(peticion)
    return ApiDeRespuesta.exito(MensajesDeConfirmacion.ENLACE_RECUPERACION_ENVIADO)


@autenticacion_router.post('/restablecer-clave')
async def restablecer_clave(
    peticion: RestablecerClavePeticion,
    servicio_auth: IAutenticacionService = Depends(get_autenticacion_service)
):
    await servicio_auth.restablecer_clave(peticion)
    return ApiDeRespuesta.exito(MensajesDeConfirmacion.CLAVE_RESTABLECIDA)


