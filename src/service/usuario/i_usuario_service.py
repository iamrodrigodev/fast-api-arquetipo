from abc import ABC, abstractmethod

class IUsuarioService(ABC):
    @abstractmethod
    async def obtener_perfil(self, usuario):
        pass
