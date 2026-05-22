import logging
from sqlalchemy.future import select
from src.model.usuario.rol import Rol
from src.config.base_de_datos import SessionLocal

logger = logging.getLogger("fastapi")

class RolRepository:
    @staticmethod
    async def buscar_por_nombre(nombre):
        async with SessionLocal() as session:
            result = await session.execute(select(Rol).filter_by(nombre=nombre))
            return result.scalars().first()

    @staticmethod
    async def guardar(rol):
        async with SessionLocal() as session:
            try:
                session.add(rol)
                await session.commit()
                await session.refresh(rol)
                logger.debug(f"Rol guardado en DB: {rol.nombre}")
                return rol
            except Exception as e:
                await session.rollback()
                logger.error(f"Error al guardar rol {rol.nombre}: {str(e)}")
                raise e
