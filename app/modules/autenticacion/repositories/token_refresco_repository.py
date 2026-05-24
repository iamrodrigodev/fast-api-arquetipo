from datetime import datetime
from sqlalchemy import select
from app.db.sesion import SessionLocal
from app.modules.autenticacion.models.token_refresco import TokenRefresco


class TokenRefrescoRepository:
    @staticmethod
    async def guardar(token_refresco: TokenRefresco) -> TokenRefresco:
        async with SessionLocal() as session:
            session.add(token_refresco)
            await session.commit()
            await session.refresh(token_refresco)
            return token_refresco

    @staticmethod
    async def buscar_activo_por_hash(token_hash: str):
        async with SessionLocal() as session:
            result = await session.execute(
                select(TokenRefresco).filter_by(token_hash=token_hash, revocado=False)
            )
            token = result.scalars().first()
            if not token:
                return None
            if token.expira_en <= datetime.now():
                return None
            return token

    @staticmethod
    async def revocar_por_hash(token_hash: str) -> bool:
        async with SessionLocal() as session:
            result = await session.execute(select(TokenRefresco).filter_by(token_hash=token_hash, revocado=False))
            token = result.scalars().first()
            if not token:
                return False
            token.revocado = True
            token.fecha_revocacion = datetime.now()
            await session.commit()
            return True

    @staticmethod
    async def revocar_todos_usuario(usuario_id: int) -> int:
        async with SessionLocal() as session:
            result = await session.execute(select(TokenRefresco).filter_by(usuario_id=usuario_id, revocado=False))
            tokens = list(result.scalars().all())
            for token in tokens:
                token.revocado = True
                token.fecha_revocacion = datetime.now()
            await session.commit()
            return len(tokens)

    @staticmethod
    async def limpiar_expirados_y_revocados() -> int:
        async with SessionLocal() as session:
            ahora = datetime.now()
            result = await session.execute(select(TokenRefresco))
            tokens = list(result.scalars().all())
            eliminados = 0
            for token in tokens:
                if token.revocado or token.expira_en <= ahora:
                    await session.delete(token)
                    eliminados += 1
            await session.commit()
            return eliminados
