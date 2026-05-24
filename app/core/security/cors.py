from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config.ajustes import ajustes

def configurar_cors(app: FastAPI):
    allow_credentials = ajustes.CORS_CREDENCIALES
    allow_origins = ajustes.cors_origenes_lista

    if allow_credentials and "*" in allow_origins:
        allow_origins = ["http://localhost:3000", "http://127.0.0.1:3000"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_credentials=allow_credentials,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Content-Disposition"]
    )
