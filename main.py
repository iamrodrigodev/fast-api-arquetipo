import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.api.enrutador import registrar_rutas
from app.core.config.ajustes import ajustes
from app.core.config.logger import configurar_logs
from app.core.exceptions.excepciones_globales import registrar_manejadores_error
from app.core.security.cors import configurar_cors
from app.db.inicializar_bd import inicializar_datos
from app.modules.autenticacion.services.impl.autenticacion_service_impl import AutenticacionServiceImpl


async def _tarea_limpieza_tokens(stop_event: asyncio.Event):
    servicio = AutenticacionServiceImpl()
    intervalo_segundos = max(1, ajustes.LIMPIEZA_TOKENS_HORAS) * 3600
    while not stop_event.is_set():
        try:
            await asyncio.wait_for(stop_event.wait(), timeout=intervalo_segundos)
        except asyncio.TimeoutError:
            await servicio.limpiar_tokens_refresco()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await inicializar_datos()
    servicio = AutenticacionServiceImpl()
    await servicio.limpiar_tokens_refresco()
    stop_event = asyncio.Event()
    tarea_limpieza = None
    if ajustes.LIMPIEZA_TOKENS_EN_API:
        tarea_limpieza = asyncio.create_task(_tarea_limpieza_tokens(stop_event))
    yield
    if tarea_limpieza is not None:
        stop_event.set()
        await tarea_limpieza


def crear_app() -> FastAPI:
    app = FastAPI(
        title="FastAPI Arquetipo",
        description="Arquetipo Idiomatico Escalable de FastAPI",
        version="1.0.0",
        lifespan=lifespan,
    )

    configurar_cors(app)
    configurar_logs(app)

    registrar_rutas(app)
    registrar_manejadores_error(app)

    return app


app = crear_app()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=ajustes.PUERTO, reload=True)
