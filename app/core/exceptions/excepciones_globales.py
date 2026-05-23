from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.responses.api_respuesta import ApiDeRespuesta
from app.core.exceptions.errores_personalizados import ExcepcionBase
from app.core.exceptions.mensajes_error import MensajesDeError
import logging

logger = logging.getLogger("fastapi")

def registrar_manejadores_error(app: FastAPI):
    @app.exception_handler(ExcepcionBase)
    async def manejar_excepcion_base(request: Request, exc: ExcepcionBase):
        logger.warning(f"Excepción de negocio: {exc.mensaje_enum.mensaje} - Detalles: {getattr(exc, 'detalles', '')}")
        return ApiDeRespuesta.error(exc.mensaje_enum, getattr(exc, 'detalles', None), errores=getattr(exc, 'errores', None), request=request)

    @app.exception_handler(RequestValidationError)
    async def manejar_validacion_pydantic(request: Request, exc: RequestValidationError):
        errores = {error['loc'][-1]: error['msg'] for error in exc.errors()}
        logger.warning(f"Error de validación de datos: {errores}")
        return ApiDeRespuesta.error(MensajesDeError.DATOS_INVALIDOS, errores=errores, request=request)

    @app.exception_handler(StarletteHTTPException)
    async def manejar_http_exception(request: Request, exc: StarletteHTTPException):
        if exc.status_code == 404:
            logger.info(f"Recurso no encontrado: {exc.detail}")
            return ApiDeRespuesta.error(MensajesDeError.RECURSO_NO_ENCONTRADO, request=request)
        elif exc.status_code == 401:
            logger.warning(f"Intento de acceso no autorizado: {exc.detail}")
            return ApiDeRespuesta.error(MensajesDeError.NO_AUTORIZADO, request=request)
        elif exc.status_code == 403:
            logger.warning(f"Acceso denegado (Forbidden): {exc.detail}")
            return ApiDeRespuesta.error(MensajesDeError.ACCESO_DENEGADO, request=request)
        return ApiDeRespuesta.error(exc.detail, codigo=exc.status_code, request=request)

    @app.exception_handler(Exception)
    async def manejar_500(request: Request, exc: Exception):
        logger.error(f"Error interno no controlado: {str(exc)}", exc_info=True)
        return ApiDeRespuesta.error(MensajesDeError.ERROR_INTERNO, request=request)
