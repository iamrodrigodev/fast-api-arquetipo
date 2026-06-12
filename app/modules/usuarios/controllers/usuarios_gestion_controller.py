from fastapi import APIRouter, Depends, Query

from app.core.dependencies.dependencias import get_usuario_service
from app.core.responses.api_respuesta import ApiDeRespuesta
from app.core.responses.mensajes_confirmacion import MensajesDeConfirmacion
from app.core.security.seguridad import (
    obtener_usuario_actual_id,
    requiere_rol,
)
from app.core.config.sistema_constantes import SistemaConstantes
from app.modules.usuarios.schemas.esquemas_usuario_gestion_peticion import (
    UsuarioGestionActualizarPeticion,
    UsuarioGestionCrearPeticion,
    UsuarioGestionEstadoPeticion,
)
from app.modules.usuarios.enums.roles_sistema import RolesSistema
from app.modules.usuarios.services.usuario_service import IUsuarioService

usuarios_gestion_router = APIRouter()


@usuarios_gestion_router.post('', dependencies=[Depends(requiere_rol(RolesSistema.ADMINISTRADOR.value))])
async def crear_usuario_gestion(
    peticion: UsuarioGestionCrearPeticion,
    administrador_id: int = Depends(obtener_usuario_actual_id),
    servicio_usuario: IUsuarioService = Depends(get_usuario_service),
):
    respuesta = await servicio_usuario.crear_usuario_gestion(peticion, administrador_id)
    return ApiDeRespuesta.creado(MensajesDeConfirmacion.USUARIO_CREADO, respuesta.model_dump())


@usuarios_gestion_router.get('', dependencies=[Depends(requiere_rol(RolesSistema.ADMINISTRADOR.value))])
async def listar_usuarios_gestion(
    pagina: int = Query(default=SistemaConstantes.PAGINACION_PAGINA_DEFECTO),
    tamano: int = Query(default=SistemaConstantes.PAGINACION_TAMANO_DEFECTO),
    correo: str | None = Query(default=None),
    rol: int | None = Query(default=None),
    estado: int | None = Query(default=None),
    servicio_usuario: IUsuarioService = Depends(get_usuario_service),
):
    respuesta = await servicio_usuario.listar_usuarios_gestion(pagina, tamano, correo, rol, estado)
    return ApiDeRespuesta.exito(MensajesDeConfirmacion.DATOS_OBTENIDOS, respuesta.model_dump())


@usuarios_gestion_router.get('/{usuario_id}', dependencies=[Depends(requiere_rol(RolesSistema.ADMINISTRADOR.value))])
async def obtener_usuario_gestion(
    usuario_id: int,
    servicio_usuario: IUsuarioService = Depends(get_usuario_service),
):
    respuesta = await servicio_usuario.obtener_usuario_gestion(usuario_id)
    return ApiDeRespuesta.exito(MensajesDeConfirmacion.DATOS_OBTENIDOS, respuesta.model_dump())


@usuarios_gestion_router.put('/{usuario_id}', dependencies=[Depends(requiere_rol(RolesSistema.ADMINISTRADOR.value))])
async def actualizar_usuario_gestion(
    usuario_id: int,
    peticion: UsuarioGestionActualizarPeticion,
    administrador_id: int = Depends(obtener_usuario_actual_id),
    servicio_usuario: IUsuarioService = Depends(get_usuario_service),
):
    respuesta = await servicio_usuario.actualizar_usuario_gestion(usuario_id, peticion, administrador_id)
    return ApiDeRespuesta.exito(MensajesDeConfirmacion.USUARIO_ACTUALIZADO, respuesta.model_dump())


@usuarios_gestion_router.patch('/{usuario_id}/estado', dependencies=[Depends(requiere_rol(RolesSistema.ADMINISTRADOR.value))])
async def cambiar_estado_usuario_gestion(
    usuario_id: int,
    peticion: UsuarioGestionEstadoPeticion,
    administrador_id: int = Depends(obtener_usuario_actual_id),
    servicio_usuario: IUsuarioService = Depends(get_usuario_service),
):
    respuesta = await servicio_usuario.cambiar_estado_usuario_gestion(usuario_id, peticion.estado, administrador_id)
    return ApiDeRespuesta.exito(MensajesDeConfirmacion.ESTADO_ACTUALIZADO, respuesta.model_dump())


@usuarios_gestion_router.delete('/{usuario_id}', dependencies=[Depends(requiere_rol(RolesSistema.ADMINISTRADOR.value))])
async def eliminar_logico_usuario_gestion(
    usuario_id: int,
    administrador_id: int = Depends(obtener_usuario_actual_id),
    servicio_usuario: IUsuarioService = Depends(get_usuario_service),
):
    await servicio_usuario.eliminar_logico_usuario_gestion(usuario_id, administrador_id)
    return ApiDeRespuesta.exito(MensajesDeConfirmacion.USUARIO_DESACTIVADO)
