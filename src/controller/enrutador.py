from fastapi import FastAPI
from src.controller.autenticacion_controller import autenticacion_router
from src.controller.usuario_controller import usuario_router
from src.controller.salud_controller import salud_router

def registrar_rutas(app: FastAPI):
    """Registra todos los routers de la aplicación."""
    app.include_router(autenticacion_router, prefix='/api/autenticacion', tags=["Autenticación"])
    app.include_router(usuario_router, prefix='/api/usuario', tags=["Usuario"])
    app.include_router(salud_router, prefix='/api/salud', tags=["Salud"])
