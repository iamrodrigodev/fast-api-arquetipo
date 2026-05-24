from datetime import datetime
from sqlalchemy import select
from app.db.sesion import SessionLocal
from app.modules.autenticacion.models.credencial_usuario import CredencialUsuario
from app.modules.autenticacion.models.estado_login_usuario import EstadoLoginUsuario
from app.modules.autenticacion.models.token_recuperacion_clave import TokenRecuperacionClave


class SeguridadCuentaRepository:
    @staticmethod
    async def obtener_credencial(usuario_id: int):
        async with SessionLocal() as session:
            result = await session.execute(select(CredencialUsuario).filter_by(usuario_id=usuario_id))
            return result.scalars().first()

    @staticmethod
    async def guardar_credencial(credencial: CredencialUsuario):
        async with SessionLocal() as session:
            entidad = await session.merge(credencial)
            await session.commit()
            await session.refresh(entidad)
            return entidad

    @staticmethod
    async def obtener_estado_login(usuario_id: int):
        async with SessionLocal() as session:
            result = await session.execute(select(EstadoLoginUsuario).filter_by(usuario_id=usuario_id))
            return result.scalars().first()

    @staticmethod
    async def guardar_estado_login(estado: EstadoLoginUsuario):
        async with SessionLocal() as session:
            entidad = await session.merge(estado)
            await session.commit()
            await session.refresh(entidad)
            return entidad

    @staticmethod
    async def revocar_tokens_recuperacion_usuario(usuario_id: int):
        async with SessionLocal() as session:
            result = await session.execute(select(TokenRecuperacionClave).filter_by(usuario_id=usuario_id, usado=False))
            tokens = list(result.scalars().all())
            ahora = datetime.now()
            for token in tokens:
                token.usado = True
                token.fecha_uso = ahora
            await session.commit()
            return len(tokens)

    @staticmethod
    async def guardar_token_recuperacion(token: TokenRecuperacionClave):
        async with SessionLocal() as session:
            session.add(token)
            await session.commit()
            await session.refresh(token)
            return token

    @staticmethod
    async def buscar_token_recuperacion_activo(token_hash: str):
        async with SessionLocal() as session:
            result = await session.execute(
                select(TokenRecuperacionClave).filter_by(token_hash=token_hash, usado=False)
            )
            entidad = result.scalars().first()
            if not entidad:
                return None
            if entidad.expira_en <= datetime.now():
                return None
            return entidad

    @staticmethod
    async def marcar_token_recuperacion_como_usado(token_id: int):
        async with SessionLocal() as session:
            result = await session.execute(select(TokenRecuperacionClave).filter_by(id=token_id, usado=False))
            entidad = result.scalars().first()
            if not entidad:
                return False
            entidad.usado = True
            entidad.fecha_uso = datetime.now()
            await session.commit()
            return True
