from enum import Enum

class MensajesDeError(Enum):
    DATOS_INVALIDOS = ("Datos de entrada inválidos", 400)
    USUARIO_NO_ENCONTRADO = ("El usuario no existe", 404)
    CREDENCIALES_INVALIDAS = ("Credenciales incorrectas", 401)
    CUENTA_BLOQUEADA = ("Cuenta bloqueada", 403)
    EMAIL_DUPLICADO = ("El correo electrónico ya está registrado", 400)
    ERROR_INTERNO = ("Error interno del servidor", 500)
    ACCESO_DENEGADO = ("Acceso denegado", 403)
    NO_AUTORIZADO = ("No autorizado", 401)
    RECURSO_NO_ENCONTRADO = ("Recurso no encontrado", 404)

    def __init__(self, mensaje, codigo):
        self.mensaje = mensaje
        self.codigo = codigo
