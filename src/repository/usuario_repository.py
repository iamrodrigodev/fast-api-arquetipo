import logging
from sqlalchemy.future import select
from src.model.usuario.usuario import Usuario
from src.config.base_de_datos import SessionLocal

logger = logging.getLogger("fastapi")

class UsuarioRepository:
    @staticmethod
    async def buscar_por_id(id):
        async with SessionLocal() as session:
            result = await session.execute(select(Usuario).filter_by(id=id))
            return result.scalars().first()

    @staticmethod
    async def buscar_por_correo(correo):
        async with SessionLocal() as session:
            result = await session.execute(select(Usuario).filter_by(correo=correo))
            return result.scalars().first()

    @staticmethod
    async def guardar(usuario):
        async with SessionLocal() as session:
            try:
                session.add(usuario)
                await session.commit()
                # Opcional, dependiendo de si se necesita refresh
                await session.refresh(usuario)
                logger.debug(f"Usuario guardado/actualizado en DB: {usuario.correo}")
                return usuario
            except Exception as e:
                await session.rollback()
                logger.error(f"Error al guardar usuario {usuario.correo}: {str(e)}")
                raise e

    @staticmethod
    async def eliminar(usuario):
        async with SessionLocal() as session:
            try:
                # Merge the detached instance before deleting
                merged_usuario = await session.merge(usuario)
                await session.delete(merged_usuario)
                await session.commit()
                logger.info(f"Usuario eliminado de DB: {usuario.correo}")
            except Exception as e:
                await session.rollback()
                logger.error(f"Error al eliminar usuario {usuario.correo}: {str(e)}")
                raise e
