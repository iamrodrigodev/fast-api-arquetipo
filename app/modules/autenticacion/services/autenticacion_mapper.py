from app.modules.autenticacion.schemas.respuesta_schema import InicioSesionRespuesta, RolRespuesta

class AutenticacionMapper:
    @staticmethod
    def de_usuario_a_inicio_sesion_respuesta(usuario, token):
        rol_dto = RolRespuesta(
            id=usuario.rol.id,
            nombre=usuario.rol.nombre
        )
        return InicioSesionRespuesta(
            id=usuario.id,
            nombre=usuario.nombre,
            apellidos=usuario.apellidos,
            correo=usuario.correo,
            foto_url=usuario.foto_url,
            rol=rol_dto,
            token=token
        )
