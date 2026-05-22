from abc import ABC, abstractmethod

class IAutenticacionService(ABC):
    @abstractmethod
    async def registrar_cuenta(self, datos):
        pass

    @abstractmethod
    async def iniciar_sesion(self, datos):
        pass

    @abstractmethod
    async def obtener_sesion(self, usuario):
        pass
