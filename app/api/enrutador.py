from fastapi import FastAPI
from app.modules.autenticacion.controllers.autenticacion_controller import autenticacion_router
from app.modules.usuarios.controllers.perfil_controller import perfil_router
from app.modules.usuarios.controllers.usuarios_gestion_controller import usuarios_gestion_router
from app.modules.estado.controllers.estado_controller import estado_router

def registrar_rutas(app: FastAPI):
    app.include_router(autenticacion_router, prefix='/api/autenticacion', tags=['Autenticacion'])
    app.include_router(perfil_router, prefix='/api/usuario', tags=['Usuario'])
    app.include_router(usuarios_gestion_router, prefix='/api/usuarios', tags=['Usuarios Gestion'])
    app.include_router(estado_router, prefix='/api/estado', tags=['Estado'])
