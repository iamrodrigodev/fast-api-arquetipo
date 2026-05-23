# dependencias.py
from app.modules.autenticacion.services.autenticacion_service import IAutenticacionService
from app.modules.autenticacion.services.impl.autenticacion_service_impl import AutenticacionServiceImpl
from app.modules.usuarios.services.usuario_service import IUsuarioService
from app.modules.usuarios.services.impl.usuario_service_impl import UsuarioServiceImpl

def get_autenticacion_service() -> IAutenticacionService:
    return AutenticacionServiceImpl()

def get_usuario_service() -> IUsuarioService:
    return UsuarioServiceImpl()
