from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config.ajustes import ajustes
from app.core.exceptions.mensajes_error import MensajesDeError

def configurar_cors(app: FastAPI):
    allow_credentials = ajustes.CORS_CREDENCIALES
    allow_origins = ajustes.cors_origenes_lista

    if allow_credentials and "*" in allow_origins:
        raise ValueError(MensajesDeError.CORS_ORIGEN_INVALIDO.mensaje)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_credentials=allow_credentials,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Content-Disposition"]
    )
