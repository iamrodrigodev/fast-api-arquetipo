from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.responses.api_respuesta import ApiDeRespuesta
from app.core.exceptions.errores_personalizados import ExcepcionBase
from app.core.exceptions.mensajes_error import MensajesDeError
import logging

logger = logging.getLogger("fastapi")


async def manejar_excepcion_base(request: Request, exc: ExcepcionBase):
    logger.warning(
        f"Excepcion de negocio: {exc.mensaje_enum.mensaje} - Detalles: {getattr(exc, 'detalles', '')}"
    )
    return ApiDeRespuesta.error(
        mensaje_enum=exc.mensaje_enum,
        detalles=getattr(exc, "detalles", None),
        errores=getattr(exc, "errores", None),
        request=request,
    )


async def manejar_validacion_pydantic(request: Request, exc: RequestValidationError):
    errores = {}
    for error in exc.errors():
        loc = error.get("loc", ())
        if loc and loc[0] == "body" and (len(loc) == 1 or isinstance(loc[-1], int)):
            errores["cuerpo"] = "Peticion mal formada"
            continue

        clave = str(loc[-1]) if loc else "campo"
        mensaje = str(error.get("msg", "Dato invalido"))
        if "required" in mensaje.lower():
            mensaje = "Este campo es obligatorio"
        errores[clave] = mensaje
    logger.warning(f"Error de validacion de datos: {errores}")
    return ApiDeRespuesta.error(MensajesDeError.DATOS_INVALIDOS, errores=errores, request=request)


async def manejar_http_exception(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        logger.info(f"Recurso no encontrado: {exc.detail}")
        return ApiDeRespuesta.error(MensajesDeError.RECURSO_NO_ENCONTRADO, request=request)
    if exc.status_code == 401:
        logger.warning(f"Intento de acceso no autorizado: {exc.detail}")
        return ApiDeRespuesta.error(MensajesDeError.NO_AUTORIZADO, request=request)
    if exc.status_code == 403:
        logger.warning(f"Acceso denegado (Forbidden): {exc.detail}")
        return ApiDeRespuesta.error(MensajesDeError.ACCESO_DENEGADO, request=request)
    if exc.status_code == 405:
        logger.info(f"Metodo HTTP no permitido: {request.method} en {request.url.path}")
        return ApiDeRespuesta.error("Metodo no permitido para este endpoint", codigo=405, request=request)
    return ApiDeRespuesta.error(exc.detail, codigo=exc.status_code, request=request)


async def manejar_500(request: Request, exc: Exception):
    logger.error(f"Error interno no controlado: {str(exc)}", exc_info=True)
    return ApiDeRespuesta.error(MensajesDeError.ERROR_INTERNO, request=request)


def registrar_manejadores_error(app: FastAPI):
    app.add_exception_handler(ExcepcionBase, manejar_excepcion_base)
    app.add_exception_handler(RequestValidationError, manejar_validacion_pydantic)
    app.add_exception_handler(StarletteHTTPException, manejar_http_exception)
    app.add_exception_handler(Exception, manejar_500)
