import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.security.cors import configurar_cors
from app.core.config.logger import configurar_logs
from app.db.inicializar_bd import inicializar_datos
from app.api.enrutador import registrar_rutas
from app.core.exceptions.excepciones_globales import registrar_manejadores_error
from app.core.config.ajustes import ajustes

@asynccontextmanager
async def lifespan(app: FastAPI):
    await inicializar_datos()
    yield

def crear_app() -> FastAPI:
    app = FastAPI(
        title="FastAPI Arquetipo",
        description="Arquetipo Idiomático Escalable de FastAPI",
        version="1.0.0",
        lifespan=lifespan
    )
    
    configurar_cors(app)
    configurar_logs(app)
    
    registrar_rutas(app)
    registrar_manejadores_error(app)
    
    return app

app = crear_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=ajustes.PUERTO, reload=True)
