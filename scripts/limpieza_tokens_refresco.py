import asyncio
import logging
import sys
import os

# Permitir importaciones del paquete 'app' desde el script standalone
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.modules.autenticacion.services.impl.autenticacion_service_impl import AutenticacionServiceImpl

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s] [SISTEMA] [%(name)s]: %(message)s")
logger = logging.getLogger("limpieza_tokens")

async def main():
    logger.info("Iniciando limpieza de tokens de refresco...")
    total = await AutenticacionServiceImpl().limpiar_tokens_refresco()
    logger.info(f"Limpieza completada. Tokens eliminados: {total}")

if __name__ == "__main__":
    asyncio.run(main())
