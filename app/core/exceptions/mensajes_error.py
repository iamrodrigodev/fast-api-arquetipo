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
    TOKEN_RECUPERACION_INVALIDO = ("Token de recuperación inválido o expirado", 400)
    ROL_NO_EXISTE = ("El rol indicado no existe", 400)
    PAGINACION_INVALIDA = ("La página debe ser mayor o igual a 1", 400)
    TAMANO_PAGINA_INVALIDO = ("El tamaño debe estar entre 1 y 100", 400)
    ESTADO_INVALIDO = ("El estado debe ser 0 o 1", 400)
    NO_PUEDE_AUTODESACTIVARSE = ("No puede desactivar su propio usuario", 400)
    DEMASIADOS_INTENTOS = ("Demasiados intentos. Intente nuevamente.", 429)
    DEMASIADAS_SOLICITUDES = ("Demasiadas solicitudes. Intente nuevamente.", 429)
    FALLO_AUTENTICACION = ("Fallo en la autenticación, intente nuevamente", 401)
    USUARIO_INACTIVO = ("Usuario inactivo", 401)
    SIN_PERMISOS = ("Acceso denegado: no tiene los permisos necesarios", 403)
    RECURSO_AJENO = ("Acceso denegado: no puede acceder a recursos de otro usuario", 403)
    JWT_CLAVE_MUY_CORTA = ("JWT_SECRET_KEY debe tener al menos 32 caracteres.", 500)
    CORS_ORIGEN_INVALIDO = ("CORS_CREDENCIALES no puede ser True si CORS_ORIGENES incluye '*'. Especifique los orígenes exactos en su archivo .env.", 500)

    def __init__(self, mensaje, codigo):
        self.mensaje = mensaje
        self.codigo = codigo
