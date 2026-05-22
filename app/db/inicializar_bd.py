import os
import bcrypt
from sqlalchemy import text
from app.db.sesion import SessionLocal, engine, Base
from app.modules.usuarios.models.rol import Rol, NombreRol
from app.modules.usuarios.models.usuario import Usuario
from app.modules.ubicacion.models.departamento import Departamento
from app.modules.ubicacion.models.provincia import Provincia
from app.modules.ubicacion.models.distrito import Distrito
import logging

logger = logging.getLogger("fastapi")

async def _asegurar_esquemas():
    async with engine.begin() as conn:
        try:
            await conn.execute(text("CREATE SCHEMA IF NOT EXISTS autenticacion;"))
            await conn.execute(text("CREATE SCHEMA IF NOT EXISTS ubicacion;"))
            logger.info("Esquemas verificados")
        except Exception as e:
            logger.error(f"Error al crear esquemas: {str(e)}")

async def _cargar_catalogos_sql():
    async with SessionLocal() as session:
        # Se requiere importar los modelos antes. En FastAPI y sqlalchemy async,
        # necesitamos primero crear las tablas.
        try:
            # Aquí se ejecutaría la inserción del catálogo SQL si está vacío.
            sql_path = os.path.join(os.path.dirname(__file__), 'sql', 'ubicacion_peru.sql')
            if os.path.exists(sql_path):
                with open(sql_path, 'r', encoding='utf-8') as f:
                    sql_content = f.read()
                    # Nota: Ejecutar sentencias completas puede variar en asyncpg.
                    await session.execute(text(sql_content))
                    await session.commit()
                    logger.info("Catálogo de ubicación (SQL) cargado exitosamente")
        except Exception as e:
            await session.rollback()
            logger.error(f"Error al cargar catálogo SQL: {str(e)}")

async def _sembrar_usuarios_base():
    # Lógica de siembra asíncrona a adaptar posteriormente.
    pass

async def inicializar_datos():
    await _asegurar_esquemas()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # await _cargar_catalogos_sql()
    # await _sembrar_usuarios_base()
