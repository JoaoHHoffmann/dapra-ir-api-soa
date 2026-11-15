from datetime import date

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field

from app.dominio.aviso import Recurso
from app.dominio.lugar import TipoDeLugar
from app.dominio.plano import Veredito
from app.dominio.relato import Necessidade, Turno


class Erro(BaseModel):
    detail: str = Field(examples=["lugar 99 não encontrado"])


NAO_ENCONTRADO = {404: {"model": Erro, "description": "Lugar não encontrado"}}
REGRA_VIOLADA = {422: {"description": "Dados inválidos ou regra do domínio violada"}}


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


class AvisoIn(BaseModel):
    recurso: Recurso = Field(examples=[Recurso.ELEVADOR])
    descricao: str = Field(min_length=1, max_length=200, examples=["Elevador da saída B parado"])
    inicio: AwareDatetime = Field(examples=["2026-11-14T08:00:00Z"])
    valido_ate: AwareDatetime = Field(examples=["2026-11-21T18:00:00Z"])


class AvisoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(examples=[1])
    lugar_id: int = Field(examples=[2])
    recurso: Recurso = Field(examples=[Recurso.ELEVADOR])
    descricao: str = Field(examples=["Elevador da saída B parado"])
    inicio: AwareDatetime = Field(examples=["2026-11-14T08:00:00Z"])
    valido_ate: AwareDatetime = Field(examples=["2026-11-21T18:00:00Z"])


class RelatoIn(BaseModel):
    data_visita: date = Field(examples=["2026-11-10"])
    turno: Turno = Field(examples=[Turno.TARDE])
    necessidade: Necessidade = Field(examples=[Necessidade.BARULHO])
    deu_certo: bool = Field(examples=[True])
    comentario: str = Field(default="", max_length=500, examples=["Sala de espera tranquila depois das 14h."])


class RelatoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(examples=[1])
    lugar_id: int = Field(examples=[1])
    data_visita: date = Field(examples=["2026-11-10"])
    turno: Turno = Field(examples=[Turno.TARDE])
    necessidade: Necessidade = Field(examples=[Necessidade.BARULHO])
    deu_certo: bool = Field(examples=[True])
    comentario: str = Field(examples=["Sala de espera tranquila depois das 14h."])


class AvisoAtivoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    recurso: Recurso = Field(examples=[Recurso.ELEVADOR])
    descricao: str = Field(examples=["Elevador da saída B parado"])
    valido_ate: AwareDatetime = Field(examples=["2026-11-21T18:00:00Z"])


class PlanoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    veredito: Veredito = Field(examples=[Veredito.DA_PRA_IR_COM_RESSALVAS])
    melhor_turno: Turno | None = Field(examples=[Turno.TARDE])
    avisos_ativos: list[AvisoAtivoOut]