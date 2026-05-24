from typing import Protocol

from app.modules.autenticacion.schemas.peticion.registro_schema import RegistroPeticion
from app.modules.autenticacion.schemas.peticion.login_schema import LoginPeticion
from app.modules.autenticacion.schemas.peticion.refrescar_token_schema import RefrescarTokenPeticion
from app.modules.autenticacion.schemas.respuesta.respuesta_schema import InicioSesionRespuesta


class IAutenticacionService(Protocol):
    async def registrar_cuenta(self, datos: RegistroPeticion) -> InicioSesionRespuesta:
        ...

    async def iniciar_sesion(self, datos: LoginPeticion) -> InicioSesionRespuesta:
        ...

    async def refrescar_token(self, datos: RefrescarTokenPeticion) -> InicioSesionRespuesta:
        ...

    async def cerrar_sesion(self, datos: RefrescarTokenPeticion) -> bool:
        ...

    async def cerrar_sesion_todos(self, usuario_id: int) -> int:
        ...

    async def limpiar_tokens_refresco(self) -> int:
        ...

    async def obtener_sesion(self, usuario) -> InicioSesionRespuesta:
        ...
