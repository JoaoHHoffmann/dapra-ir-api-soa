from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from app.dominio.aviso import Aviso
from app.dominio.relato import Necessidade, Relato, Turno


class Veredito(str, Enum):
    DA_PRA_IR = "DA_PRA_IR"
    DA_PRA_IR_COM_RESSALVAS = "DA_PRA_IR_COM_RESSALVAS"
    MELHOR_NAO_IR = "MELHOR_NAO_IR"
    SEM_RELATOS = "SEM_RELATOS"


@dataclass(frozen=True)
class Plano:
    veredito: Veredito
    melhor_turno: Turno | None
    avisos_ativos: list[Aviso]


def montar_plano(avisos: list[Aviso], relatos: list[Relato],
                 necessidade: Necessidade, momento: datetime) -> Plano:
    avisos_ativos = [a for a in avisos if a.esta_ativo(momento)]
    relevantes = [r for r in relatos if r.necessidade == necessidade]
    sucessos = [r for r in relevantes if r.deu_certo]

    if not relevantes:
        veredito = Veredito.SEM_RELATOS
    elif len(sucessos) * 2 < len(relevantes):  # mais da metade disse "não deu"
        veredito = Veredito.MELHOR_NAO_IR
    elif avisos_ativos:
        veredito = Veredito.DA_PRA_IR_COM_RESSALVAS
    else:
        veredito = Veredito.DA_PRA_IR

    return Plano(veredito, _melhor_turno(sucessos), avisos_ativos)


def _melhor_turno(sucessos: list[Relato]) -> Turno | None:
    # o turno com mais "deu certo"; em empate, vale o mais cedo
    if not sucessos:
        return None
    return max(Turno, key=lambda t: sum(1 for r in sucessos if r.turno == t))