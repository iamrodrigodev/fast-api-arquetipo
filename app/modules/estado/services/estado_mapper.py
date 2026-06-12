from app.modules.estado.schemas.estado_schema import EstadoRespuesta

class EstadoMapper:
    @staticmethod
    def de_estado_a_estado_respuesta(servicio: str, version: str, estado: str):
        return EstadoRespuesta(
            servicio=servicio,
            version=version,
            estado=estado
        )