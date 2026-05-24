import asyncio

from app.modules.autenticacion.services.impl.autenticacion_service_impl import AutenticacionServiceImpl

async def main():
    total = await AutenticacionServiceImpl().limpiar_tokens_refresco()
    print(f"Limpieza tokens_refresco completada. Eliminados={total}")


if __name__ == "__main__":
    asyncio.run(main())
