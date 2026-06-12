import logging
from app.utils.datos_sensibles import sanitizar_campos_sensibles
from app.db.sesion import SessionLocal
from app.modules.estado.models.registro_auditoria import RegistroAuditoria

logger = logging.getLogger("fastapi")

async def registrar_evento_auditoria(evento: str, resultado: str, **campos):
    campos_saneados = sanitizar_campos_sensibles(campos)
    
    # Log por consola (opcional, pero útil para depuración)
    partes = [f"evento={evento}", f"resultado={resultado}"]
    for clave, valor in campos_saneados.items():
        partes.append(f"{clave}={valor}")
    logger.info("[AUDITORIA] " + " ".join(partes))

    # Inserción asíncrona en base de datos
    try:
        async with SessionLocal() as session:
            registro = RegistroAuditoria(
                evento=evento,
                resultado=resultado,
                campos=campos_saneados
            )
            session.add(registro)
            await session.commit()
    except Exception as e:
        logger.error(f"Error guardando auditoria en BD: {e}")
