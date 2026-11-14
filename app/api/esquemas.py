from pydantic import BaseModel, ConfigDict, Field

from app.dominio.lugar import TipoDeLugar


class Erro(BaseModel):
    detail: str = Field(examples=["lugar 99 não encontrado"])


class LugarIn(BaseModel):
    nome: str = Field(min_length=1, max_length=100, examples=["UBS Jardim Esperança"])
    tipo: TipoDeLugar = Field(examples=[TipoDeLugar.UBS])
    bairro: str = Field(min_length=1, max_length=60, examples=["Jardim Esperança"])
    como_e: str = Field(default="", examples=["Entrada lateral com rampa. Mais tranquilo à tarde."])


class LugarOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(examples=[1])
    nome: str = Field(examples=["UBS Jardim Esperança"])
    tipo: TipoDeLugar = Field(examples=[TipoDeLugar.UBS])
    bairro: str = Field(examples=["Jardim Esperança"])
    como_e: str = Field(examples=["Entrada lateral com rampa. Mais tranquilo à tarde."])