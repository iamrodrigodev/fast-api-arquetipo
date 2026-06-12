from app.modules.usuarios.schemas.respuesta.esquemas_usuario import (
    DireccionPerfilRespuesta,
    PerfilRespuesta,
    RolRespuesta,
)
from app.modules.usuarios.schemas.respuesta.esquemas_usuario_gestion_respuesta import UsuarioGestionRespuesta


class UsuarioMapper:
    @staticmethod
    def de_usuario_a_perfil_respuesta(usuario):
        rol_dto = RolRespuesta(
            id=usuario.rol.id,
            nombre=usuario.rol.nombre
        )

        direccion_dto = None
        if getattr(usuario, "direccion", None):
            distrito = getattr(usuario.direccion, "distrito", None)
            provincia = getattr(distrito, "provincia", None) if distrito else None
            departamento = getattr(provincia, "departamento", None) if provincia else None
            direccion_dto = DireccionPerfilRespuesta(
                direccion_exacta=usuario.direccion.direccion_exacta,
                referencia=usuario.direccion.referencia,
                codigo_postal=usuario.direccion.codigo_postal,
                distrito_id=usuario.direccion.distrito_id,
                distrito_nombre=getattr(distrito, "nombre", None),
                provincia_nombre=getattr(provincia, "nombre", None),
                departamento_nombre=getattr(departamento, "nombre", None),
            )

        return PerfilRespuesta(
            id=usuario.id,
            nombre=usuario.nombre,
            apellidos=usuario.apellidos,
            correo=usuario.correo,
            telefono=usuario.telefono,
            foto_url=usuario.foto_url,
            rol=rol_dto,
            direccion=direccion_dto,
        )

    @staticmethod
    def de_usuario_a_gestion_respuesta(usuario):
        return UsuarioGestionRespuesta(
            id=usuario.id,
            nombre=usuario.nombre,
            apellidos=usuario.apellidos,
            correo=usuario.correo,
            telefono=usuario.telefono,
            foto_url=usuario.foto_url,
            estado=int(usuario.estado),
            rol=RolRespuesta(id=usuario.rol.id, nombre=usuario.rol.nombre),
            fecha_creacion=usuario.fecha_creacion,
            fecha_actualizacion=usuario.fecha_actualizacion,
        )
