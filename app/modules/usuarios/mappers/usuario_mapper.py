from app.modules.usuarios.schemas.respuesta.esquemas_usuario import PerfilRespuesta, RolRespuesta

class UsuarioMapper:
    @staticmethod
    def de_usuario_a_perfil_respuesta(usuario):
        rol_dto = RolRespuesta(
            id=usuario.rol.id,
            nombre=usuario.rol.nombre
        )
        return PerfilRespuesta(
            id=usuario.id,
            nombre=usuario.nombre,
            apellidos=usuario.apellidos,
            correo=usuario.correo,
            telefono=usuario.telefono,
            foto_url=usuario.foto_url,
            rol=rol_dto
        )
