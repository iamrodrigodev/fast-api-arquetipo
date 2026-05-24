import logging
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError
from app.modules.usuarios.models.usuario import Usuario
from app.db.sesion import SessionLocal

logger = logging.getLogger("fastapi")

class UsuarioRepository:
    @staticmethod
    async def buscar_por_id(id):
        async with SessionLocal() as session:
            result = await session.execute(
                select(Usuario)
                .options(selectinload(Usuario.rol), selectinload(Usuario.direccion))
                .filter_by(id=id)
            )
            return result.scalars().first()

    @staticmethod
    async def buscar_por_correo(correo):
        async with SessionLocal() as session:
            result = await session.execute(
                select(Usuario)
                .options(selectinload(Usuario.rol), selectinload(Usuario.direccion))
                .filter_by(correo=correo)
            )
            return result.scalars().first()

    @staticmethod
    async def guardar(usuario):
        async with SessionLocal() as session:
            correo_seguro = getattr(usuario, "correo", "<sin_correo>")
            try:
                if getattr(usuario, "id", None) is None:
                    session.add(usuario)
                    entidad = usuario
                else:
                    entidad = await session.merge(usuario)
                await session.commit()
                await session.refresh(entidad)
                logger.debug(f"Usuario guardado/actualizado en DB: {entidad.correo}")
                return entidad
            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Error al guardar usuario {correo_seguro}: {str(e)}")
                raise

    @staticmethod
    async def eliminar(usuario):
        async with SessionLocal() as session:
            correo_seguro = getattr(usuario, "correo", "<sin_correo>")
            try:
                merged_usuario = await session.merge(usuario)
                await session.delete(merged_usuario)
                await session.commit()
                logger.info(f"Usuario eliminado de DB: {usuario.correo}")
            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Error al eliminar usuario {correo_seguro}: {str(e)}")
                raise
