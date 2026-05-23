from fastapi import FastAPI
from app.modules.autenticacion.controllers.autenticacion_controller import autenticacion_router
from app.modules.usuarios.controllers.usuario_controller import usuario_router
from app.modules.salud.controllers.salud_controller import salud_router

def registrar_rutas(app: FastAPI):
    app.include_router(autenticacion_router, prefix='/api/autenticacion', tags=["Autenticación"])
    app.include_router(usuario_router, prefix='/api/usuario', tags=["Usuario"])
    app.include_router(salud_router, prefix='/api/salud', tags=["Salud"])
