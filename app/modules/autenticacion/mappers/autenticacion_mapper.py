from app.modules.autenticacion.schemas.respuesta.respuesta_schema import InicioSesionRespuesta, RolRespuesta


class AutenticacionMapper:
    @staticmethod
    def de_usuario_a_inicio_sesion_respuesta(usuario, token_acceso, token_refresco, expira_en_segundos: int):
        rol_dto = RolRespuesta(id=usuario.rol.id, nombre=usuario.rol.nombre)
        return InicioSesionRespuesta(
            id=usuario.id,
            nombre=usuario.nombre,
            apellidos=usuario.apellidos,
            correo=usuario.correo,
            foto_url=usuario.foto_url,
            rol=rol_dto,
            token_acceso=token_acceso,
            token_refresco=token_refresco,
            expira_en_segundos=expira_en_segundos,
        )
