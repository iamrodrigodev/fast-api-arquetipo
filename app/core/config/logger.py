import logging
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

class InyectorTrazabilidadMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.id_trazabilidad = str(uuid.uuid4())
        request.state.cliente_ip = request.client.host if request.client else '0.0.0.0'
        
        response = await call_next(request)
        return response

class ContextFilter(logging.Filter):
    def filter(self, record):
        # En logs asíncronos puros es más complejo inyectar el request en todos lados,
        # pero para mantener la firma se puede usar contextvars si fuera estricto.
        # Por simplicidad, seteamos valores por defecto aquí.
        if not hasattr(record, 'id_trazabilidad'):
            record.id_trazabilidad = 'SISTEMA'
        if not hasattr(record, 'cliente_ip'):
            record.cliente_ip = '0.0.0.0'
        return True

def configurar_logs(app):
    formato = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(id_trazabilidad)s] [%(cliente_ip)s] [%(name)s]: %(message)s'
    )

    inyector = ContextFilter()

    handler_consola = logging.StreamHandler()
    handler_consola.setFormatter(formato)
    handler_consola.addFilter(inyector)

    logger = logging.getLogger("fastapi")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler_consola)
    
    app.add_middleware(InyectorTrazabilidadMiddleware)
