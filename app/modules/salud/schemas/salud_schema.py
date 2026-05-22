from pydantic import BaseModel

class SaludRespuesta(BaseModel):
    servicio: str
    version: str
    estado: str