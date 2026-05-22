from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.config.configuracion_cors import configurar_cors
from src.config.configuracion_logs import configurar_logs
from src.config.datos_iniciales import inicializar_datos

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Lógica de inicio
    await inicializar_datos()
    yield
    # Lógica de apagado

class IniciadorApp:
    @staticmethod
    def configurar() -> FastAPI:
        app = FastAPI(
            title="FastAPI Arquetipo",
            description="Arquetipo migrado de Flask a FastAPI",
            version="1.0.0",
            lifespan=lifespan
        )
        
        # Middlewares y utilidades
        configurar_cors(app)
        configurar_logs(app)
        
        # Las rutas y manejadores de error se registrarán en main.py o importando sus enrutadores aquí
        
        return app
