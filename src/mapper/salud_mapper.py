from src.controller.dto.salud.respuesta.salud_respuesta import SaludRespuesta

class SaludMapper:
    @staticmethod
    def de_estado_a_salud_respuesta(servicio: str, version: str, estado: str):
        return SaludRespuesta(
            servicio=servicio,
            version=version,
            estado=estado
        )