from fastapi import Request
from app.core.exceptions.errores_personalizados import ExcepcionDeNegocio
from app.core.exceptions.mensajes_error import MensajesDeError
from app.utils.rate_limit_util import limitador_memoria
from app.core.config.ajustes import ajustes


def _ip(request: Request) -> str:
    return request.client.host if request.client else "0.0.0.0"


def validar_rate_limit_login(request: Request, correo: str):
    if ajustes.ENTORNO.lower() in {"test", "testing"}:
        return
    if not limitador_memoria.permitido(f"login_ip:{_ip(request)}", 20, 60):
        raise ExcepcionDeNegocio(MensajesDeError.DEMASIADOS_INTENTOS)
    if not limitador_memoria.permitido(f"login_correo:{correo.lower()}", 10, 60):
        raise ExcepcionDeNegocio(MensajesDeError.DEMASIADOS_INTENTOS)


def validar_rate_limit_refresh(request: Request, token_refresco: str):
    if ajustes.ENTORNO.lower() in {"test", "testing"}:
        return
    if not limitador_memoria.permitido(f"refresh_ip:{_ip(request)}", 30, 60):
        raise ExcepcionDeNegocio(MensajesDeError.DEMASIADAS_SOLICITUDES)
    sufijo = token_refresco[-12:] if token_refresco else "vacio"
    if not limitador_memoria.permitido(f"refresh_token:{sufijo}", 15, 60):
        raise ExcepcionDeNegocio(MensajesDeError.DEMASIADAS_SOLICITUDES)


def validar_rate_limit_recuperacion(request: Request, correo: str):
    if ajustes.ENTORNO.lower() in {"test", "testing"}:
        return
    if not limitador_memoria.permitido(f"recup_ip:{_ip(request)}", 15, 60):
        raise ExcepcionDeNegocio(MensajesDeError.DEMASIADAS_SOLICITUDES)
    if not limitador_memoria.permitido(f"recup_correo:{correo.lower()}", 6, 300):
        raise ExcepcionDeNegocio(MensajesDeError.DEMASIADAS_SOLICITUDES)

from app.modules.autenticacion.schemas.peticion.login_schema import LoginPeticion
from app.modules.autenticacion.schemas.peticion.refrescar_token_schema import RefrescarTokenPeticion
from app.modules.autenticacion.schemas.peticion.recuperacion_clave_schema import SolicitarRecuperacionClavePeticion

def dep_rate_limit_login(request: Request, peticion: LoginPeticion):
    validar_rate_limit_login(request, peticion.correo)

def dep_rate_limit_refresh(request: Request, peticion: RefrescarTokenPeticion):
    validar_rate_limit_refresh(request, peticion.token_refresco)

def dep_rate_limit_recuperacion(request: Request, peticion: SolicitarRecuperacionClavePeticion):
    validar_rate_limit_recuperacion(request, peticion.correo)

def validar_rate_limit_inicio_aplicacion(request: Request, codigo: str):
    if ajustes.ENTORNO.lower() in {"test", "testing"}:
        return
    if not limitador_memoria.permitido(f"eval_ini_ip:{_ip(request)}", 30, 60):
        raise ExcepcionDeNegocio(MensajesDeError.DEMASIADAS_SOLICITUDES)
    if not limitador_memoria.permitido(f"eval_ini_codigo:{(codigo or '').upper()}", 20, 60):
        raise ExcepcionDeNegocio(MensajesDeError.DEMASIADAS_SOLICITUDES)


def validar_rate_limit_responder(request: Request, aplicacion_id: int):
    if ajustes.ENTORNO.lower() in {"test", "testing"}:
        return
    if not limitador_memoria.permitido(f"eval_resp_ip:{_ip(request)}", 120, 60):
        raise ExcepcionDeNegocio(MensajesDeError.DEMASIADAS_SOLICITUDES)
    if not limitador_memoria.permitido(f"eval_resp_apl:{aplicacion_id}", 80, 60):
        raise ExcepcionDeNegocio(MensajesDeError.DEMASIADAS_SOLICITUDES)


def validar_rate_limit_finalizar(request: Request, aplicacion_id: int):
    if ajustes.ENTORNO.lower() in {"test", "testing"}:
        return
    if not limitador_memoria.permitido(f"eval_fin_ip:{_ip(request)}", 40, 60):
        raise ExcepcionDeNegocio(MensajesDeError.DEMASIADAS_SOLICITUDES)
    if not limitador_memoria.permitido(f"eval_fin_apl:{aplicacion_id}", 10, 60):
        raise ExcepcionDeNegocio(MensajesDeError.DEMASIADAS_SOLICITUDES)


