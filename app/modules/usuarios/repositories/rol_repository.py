import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select

from app.db.sesion import SessionLocal
from app.modules.usuarios.models.rol import Rol

logger = logging.getLogger("fastapi")


class RolRepository:
    @staticmethod
    async def buscar_por_nombre(nombre):
        async with SessionLocal() as session:
            result = await session.execute(select(Rol).filter_by(nombre=nombre))
            return result.scalars().first()

    @staticmethod
    async def buscar_por_id(rol_id: int):
        async with SessionLocal() as session:
            result = await session.execute(select(Rol).filter_by(id=rol_id))
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
            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Error al guardar rol {rol.nombre}: {str(e)}")
                raise
