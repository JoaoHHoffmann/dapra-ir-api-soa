from dataclasses import dataclass
from datetime import date
from enum import Enum

from app.dominio.erros import RegraViolada


class Turno(str, Enum):
    MANHA = "MANHA"
    TARDE = "TARDE"
    NOITE = "NOITE"


class Necessidade(str, Enum):
    BARULHO = "BARULHO"
    CADEIRA_DE_RODAS = "CADEIRA_DE_RODAS"
    MOBILIDADE_REDUZIDA = "MOBILIDADE_REDUZIDA"


@dataclass(frozen=True)
class Relato:
    data_visita: date
    turno: Turno
    necessidade: Necessidade
    deu_certo: bool
    comentario: str = ""

    def __post_init__(self):
        if self.data_visita > date.today():
            raise RegraViolada("a data da visita não pode estar no futuro")