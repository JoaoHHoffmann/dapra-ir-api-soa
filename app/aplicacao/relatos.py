from sqlalchemy import select
from sqlalchemy.orm import Session

from app.aplicacao.lugares import buscar_lugar
from app.dominio.relato import Relato
from app.infraestrutura.modelos import RelatoORM


def registrar_relato(sessao: Session, lugar_id: int, relato: Relato) -> RelatoORM:
    buscar_lugar(sessao, lugar_id)
    orm = RelatoORM(lugar_id=lugar_id, data_visita=relato.data_visita, turno=relato.turno.value,
                    necessidade=relato.necessidade.value, deu_certo=relato.deu_certo,
                    comentario=relato.comentario)
    sessao.add(orm)
    sessao.commit()
    sessao.refresh(orm)
    return orm


def listar_relatos(sessao: Session, lugar_id: int) -> list[RelatoORM]:
    buscar_lugar(sessao, lugar_id)
    consulta = (select(RelatoORM)
                .where(RelatoORM.lugar_id == lugar_id)
                .order_by(RelatoORM.data_visita.desc()))
    return list(sessao.scalars(consulta))