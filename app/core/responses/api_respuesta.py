from fastapi.responses import JSONResponse
from fastapi import Request
from datetime import datetime

class ApiDeRespuesta:
    @staticmethod
    def exito(mensaje_enum, datos=None, codigo=200):
        mensaje = mensaje_enum.value if hasattr(mensaje_enum, 'value') else mensaje_enum

        respuesta = {
            "estado": codigo,
            "mensaje": mensaje,
            "datos": datos
        }

        return JSONResponse(
            status_code=codigo,
            content={k: v for k, v in respuesta.items() if v is not None}
        )

    from typing import Optional
    @staticmethod
    def error(mensaje_enum, detalles=None, codigo=None, errores=None, request: Optional[Request] = None):
        ahora = datetime.now()

        if hasattr(mensaje_enum, 'mensaje'):
            mensaje = mensaje_enum.mensaje
            codigo_final = codigo or mensaje_enum.codigo
        else:
            mensaje = str(mensaje_enum)
            codigo_final = codigo or 400

        respuesta = {
            "estado": codigo_final,
            "mensaje": mensaje,
            "detalles": detalles,
            "ruta": request.url.path if request else None,
            "fecha": ahora.strftime("%Y-%m-%d"),
            "hora": ahora.strftime("%H:%M:%S"),
            "errores": errores
        }

        return JSONResponse(
            status_code=codigo_final,
            content={k: v for k, v in respuesta.items() if v is not None}
        )

    @staticmethod
    def creado(mensaje_enum, datos=None):
        return ApiDeRespuesta.exito(mensaje_enum, datos, 201)
