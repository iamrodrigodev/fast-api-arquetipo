import json
import logging
import uuid
from datetime import datetime, UTC

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.core.config.ajustes import ajustes


class InyectorTrazabilidadMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.id_trazabilidad = str(uuid.uuid4())
        request.state.cliente_ip = request.client.host if request.client else "0.0.0.0"
        request.state.ruta = request.url.path
        request.state.metodo = request.method
        response = await call_next(request)
        return response


class ContextFilter(logging.Filter):
    def filter(self, record):
        if not hasattr(record, "id_trazabilidad"):
            record.id_trazabilidad = "SISTEMA"
        if not hasattr(record, "cliente_ip"):
            record.cliente_ip = "0.0.0.0"
        if not hasattr(record, "ruta"):
            record.ruta = "-"
        if not hasattr(record, "metodo"):
            record.metodo = "-"
        return True


class JsonFormatter(logging.Formatter):
    def format(self, record):
        payload = {
            "timestamp": datetime.now(UTC).isoformat(),
            "nivel": record.levelname,
            "logger": record.name,
            "mensaje": record.getMessage(),
            "id_trazabilidad": getattr(record, "id_trazabilidad", "SISTEMA"),
            "cliente_ip": getattr(record, "cliente_ip", "0.0.0.0"),
            "ruta": getattr(record, "ruta", "-"),
            "metodo": getattr(record, "metodo", "-"),
        }
        return json.dumps(payload, ensure_ascii=False)


def configurar_logs(app):
    inyector = ContextFilter()

    handler_consola = logging.StreamHandler()
    if ajustes.LOG_FORMAT.lower() == "json":
        handler_consola.setFormatter(JsonFormatter())
    else:
        formato = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(id_trazabilidad)s] [%(cliente_ip)s] [%(name)s]: %(message)s"
        )
        handler_consola.setFormatter(formato)

    handler_consola.addFilter(inyector)

    logger = logging.getLogger("fastapi")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    logger.propagate = False
    logger.addHandler(handler_consola)

    app.add_middleware(InyectorTrazabilidadMiddleware)
