from dataclasses import dataclass
from enum import Enum

from app.dominio.erros import RegraViolada


class TipoDeLugar(str, Enum):
    UBS = "UBS"
    ESCOLA = "ESCOLA"
    ESTACAO = "ESTACAO"
    DENTISTA = "DENTISTA"
    OUTRO = "OUTRO"


@dataclass(frozen=True)
class Lugar:
    nome: str
    tipo: TipoDeLugar
    bairro: str
    como_e: str = ""

    def __post_init__(self):
        if not self.nome.strip():
            raise RegraViolada("o lugar precisa ter um nome")
        if not self.bairro.strip():
            raise RegraViolada("o lugar precisa ter um bairro")
        object.__setattr__(self, "nome", self.nome.strip())
        object.__setattr__(self, "bairro", self.bairro.strip())