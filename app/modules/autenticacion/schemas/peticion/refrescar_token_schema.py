from pydantic import BaseModel, Field, field_validator
from pydantic_core import PydanticCustomError


class RefrescarTokenPeticion(BaseModel):
    token_refresco: str = Field(..., min_length=20)

    @field_validator("token_refresco")
    @classmethod
    def validar_token_refresco(cls, v: str) -> str:
        if not v or len(v.strip()) == 0:
            raise PydanticCustomError("value_error", "El token de refresco es obligatorio")
        return v.strip()
