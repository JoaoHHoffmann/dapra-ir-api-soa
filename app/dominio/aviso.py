from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from app.dominio.erros import RegraViolada


class Recurso(str, Enum):
    ELEVADOR = "ELEVADOR"
    RAMPA = "RAMPA"
    BANHEIRO_ADAPTADO = "BANHEIRO_ADAPTADO"
    ENTRADA = "ENTRADA"
    OUTRO = "OUTRO"


@dataclass(frozen=True)
class Aviso:
    recurso: Recurso
    descricao: str
    inicio: datetime
    valido_ate: datetime

    def __post_init__(self):
        if self.valido_ate <= self.inicio:
            raise RegraViolada("a validade do aviso deve ser depois do início")

    def esta_ativo(self, momento: datetime) -> bool:
        # aviso vencido não vale mais: é assim que a informação não fica desatualizada
        return self.inicio <= momento < self.valido_ate