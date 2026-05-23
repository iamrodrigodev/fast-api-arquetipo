import os
import bcrypt
from sqlalchemy import text
from app.db.sesion import SessionLocal, engine, Base
from app.modules.usuarios.models.rol import Rol
from app.modules.usuarios.enums.nombre_rol import NombreRol
from app.modules.usuarios.models.usuario import Usuario
from app.modules.ubicacion.models.departamento import Departamento
from app.modules.ubicacion.models.provincia import Provincia
from app.modules.ubicacion.models.distrito import Distrito
import logging


_ = (bcrypt, Rol, NombreRol, Usuario, Departamento, Provincia, Distrito)

logger = logging.getLogger("fastapi")

async def _asegurar_esquemas():
    async with engine.begin() as conn:
        try:
            await conn.execute(text("CREATE SCHEMA IF NOT EXISTS autenticacion;"))
            await conn.execute(text("CREATE SCHEMA IF NOT EXISTS ubicacion;"))
            logger.info("Esquemas verificados")
        except Exception as e:
            logger.error(f"Error al crear esquemas: {str(e)}")

from sqlalchemy.exc import IntegrityError

async def cargar_catalogos_sql():
    async with SessionLocal() as session:
        try:
            sql_path = os.path.join(os.path.dirname(__file__), 'sql', 'ubicacion_peru.sql')
            if os.path.exists(sql_path):
                with open(sql_path, 'r', encoding='utf-8') as f:
                    sql_content = f.read()
                    statements = [s.strip() for s in sql_content.split(';') if s.strip()]
                    for statement in statements:
                        await session.execute(text(statement))
                    await session.commit()
                    logger.info("Catálogo de ubicación (SQL) cargado exitosamente")
            else:
                logger.warning(f"Archivo SQL no encontrado en la ruta: {sql_path}")
        except IntegrityError:
            await session.rollback()
            logger.info("Catálogo de ubicación ya existe (se ignoró el insert duplicado)")
        except Exception as e:
            await session.rollback()
            logger.error(f"Error al cargar catálogo SQL: {str(e)}")

async def sembrar_usuarios_base():
    async with SessionLocal() as session:
        try:
            sql_path = os.path.join(os.path.dirname(__file__), 'sql', 'usuarios_semilla.sql')
            if os.path.exists(sql_path):
                with open(sql_path, 'r', encoding='utf-8') as f:
                    sql_content = f.read()
                    statements = [s.strip() for s in sql_content.split(';') if s.strip()]
                    for statement in statements:
                        await session.execute(text(statement))
                    await session.commit()
                    logger.info("Usuarios semilla cargados exitosamente (Admin y Usuario)")
            else:
                logger.warning(f"Archivo SQL de usuarios no encontrado: {sql_path}")
        except Exception as e:
            await session.rollback()
            logger.error(f"Error al cargar usuarios semilla: {str(e)}")

async def inicializar_datos():
    await _asegurar_esquemas()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await cargar_catalogos_sql()
    await sembrar_usuarios_base()
