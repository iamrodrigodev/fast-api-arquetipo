from pydantic import BaseModel

class EstadoRespuesta(BaseModel):
    servicio: str
    version: str
    estado: str