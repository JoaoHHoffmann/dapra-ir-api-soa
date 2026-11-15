from datetime import datetime

from sqlalchemy.orm import Session

from app.aplicacao.lugares import buscar_lugar
from app.dominio.aviso import Aviso, Recurso
from app.dominio.plano import Plano, montar_plano
from app.dominio.relato import Necessidade, Relato, Turno


def consultar_plano(sessao: Session, lugar_id: int, necessidade: Necessidade,
                    momento: datetime) -> Plano:
    lugar = buscar_lugar(sessao, lugar_id)
    avisos = [Aviso(Recurso(a.recurso), a.descricao, a.inicio, a.valido_ate)
              for a in lugar.avisos]
    relatos = [Relato(r.data_visita, Turno(r.turno), Necessidade(r.necessidade),
                      r.deu_certo, r.comentario)
               for r in lugar.relatos]
    return montar_plano(avisos, relatos, necessidade, momento)