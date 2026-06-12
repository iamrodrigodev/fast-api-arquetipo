import logging

from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

from app.core.config.ajustes import ajustes

logger = logging.getLogger('fastapi')


def verificar_revision_alembic() -> bool:
    try:
        cfg = Config('alembic.ini')
        script = ScriptDirectory.from_config(cfg)
        heads = script.get_heads()
        sync_url = ajustes.DATABASE_URL.replace('+asyncpg', '')
        engine = create_engine(sync_url)
        with engine.connect() as conn:
            current = MigrationContext.configure(conn).get_current_heads()
        ok = set(current) == set(heads)
        if not ok:
            logger.warning(f"[MIGRACION] DB fuera de head. actual={current} esperado={heads}")
        return ok
    except (SQLAlchemyError, OSError, RuntimeError, ValueError) as exc:
        logger.warning(f"[MIGRACION] No se pudo verificar head de Alembic: {exc.__class__.__name__}: {exc}")
        return False
