from enum import Enum


class MensajesDeConfirmacion(Enum):
    OPERACION_EXITOSA = "Operación realizada exitosamente"
    LOGIN_EXITOSO = "Inicio de sesión exitoso"
    CUENTA_REGISTRADA = "Cuenta registrada exitosamente"
    DATOS_OBTENIDOS = "Datos obtenidos exitosamente"
    SESION_CERRADA = "Sesión cerrada exitosamente"
    SISTEMA_EN_LINEA = "Sistema en línea y funcionando"
    ENLACE_RECUPERACION_ENVIADO = "Si el correo existe, se enviará un enlace de recuperación"
    CLAVE_RESTABLECIDA = "Clave restablecida exitosamente"
    USUARIO_CREADO = "Usuario creado correctamente"
    USUARIO_ACTUALIZADO = "Usuario actualizado correctamente"
    ESTADO_ACTUALIZADO = "Estado actualizado correctamente"
    USUARIO_DESACTIVADO = "Usuario desactivado correctamente"
