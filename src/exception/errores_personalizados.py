from src.exception.mensajes_error import MensajesDeError

class ExcepcionBase(Exception):
    def __init__(self, mensaje_enum: MensajesDeError, detalles=None, errores=None):
        super().__init__(mensaje_enum.mensaje)
        self.mensaje_enum = mensaje_enum
        self.detalles = detalles
        self.errores = errores

class ExcepcionDeRecursoNoEncontrado(ExcepcionBase):
    def __init__(self, detalles=None):
        super().__init__(MensajesDeError.RECURSO_NO_ENCONTRADO, detalles)

class ExcepcionDeNegocio(ExcepcionBase):
    def __init__(self, mensaje_enum: MensajesDeError, detalles=None, errores=None):
        super().__init__(mensaje_enum, detalles, errores)
