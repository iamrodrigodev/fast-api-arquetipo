import logging
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.db.sesion import SessionLocal
from app.modules.ubicacion.models.distrito import Distrito
from app.modules.ubicacion.models.provincia import Provincia
from app.modules.usuarios.models.usuario import Usuario
from app.modules.usuarios.models.usuario_direccion import UsuarioDireccion
from app.utils.datos_sensibles import enmascarar_correo

logger = logging.getLogger("fastapi")


class UsuarioRepository:
    @staticmethod
    def _query_base():
        return (
            select(Usuario)
            .options(
                selectinload(Usuario.rol),
                selectinload(Usuario.direccion)
                .selectinload(UsuarioDireccion.distrito)
                .selectinload(Distrito.provincia)
                .selectinload(Provincia.departamento),
            )
        )

    @staticmethod
    async def buscar_por_id(id):
        async with SessionLocal() as session:
            result = await session.execute(UsuarioRepository._query_base().filter_by(id=id))
            return result.scalars().first()

    @staticmethod
    async def buscar_por_correo(correo):
        async with SessionLocal() as session:
            result = await session.execute(UsuarioRepository._query_base().filter_by(correo=correo))
            return result.scalars().first()

    @staticmethod
    async def listar_paginado(pagina: int, tamano: int, correo: str | None, rol: int | None, estado: int | None):
        async with SessionLocal() as session:
            query = UsuarioRepository._query_base()
            count_query = select(func.count(Usuario.id))

            if correo:
                patron = f"%{correo.strip().lower()}%"
                query = query.where(func.lower(Usuario.correo).like(patron))
                count_query = count_query.where(func.lower(Usuario.correo).like(patron))
            if rol is not None:
                query = query.where(Usuario.rol_id == rol)
                count_query = count_query.where(Usuario.rol_id == rol)
            if estado is not None:
                query = query.where(Usuario.estado == estado)
                count_query = count_query.where(Usuario.estado == estado)

            query = query.order_by(Usuario.id.desc()).offset((pagina - 1) * tamano).limit(tamano)

            total_result = await session.execute(count_query)
            total = int(total_result.scalar() or 0)
            result = await session.execute(query)
            return result.scalars().all(), total

    @staticmethod
    async def guardar(usuario):
        async with SessionLocal() as session:
            correo_seguro = enmascarar_correo(getattr(usuario, "correo", None))
            try:
                if getattr(usuario, "id", None) is None:
                    session.add(usuario)
                    entidad = usuario
                else:
                    entidad = await session.merge(usuario)
                await session.commit()
                await session.refresh(entidad)
                logger.debug(f"Usuario guardado/actualizado en DB: {enmascarar_correo(entidad.correo)}")
                return entidad
            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Error al guardar usuario {correo_seguro}: {str(e)}")
                raise

    @staticmethod
    async def eliminar(usuario):
        async with SessionLocal() as session:
            correo_seguro = enmascarar_correo(getattr(usuario, "correo", None))
            try:
                merged_usuario = await session.merge(usuario)
                await session.delete(merged_usuario)
                await session.commit()
                logger.info(f"Usuario eliminado de DB: {enmascarar_correo(usuario.correo)}")
            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Error al eliminar usuario {correo_seguro}: {str(e)}")
                raise
