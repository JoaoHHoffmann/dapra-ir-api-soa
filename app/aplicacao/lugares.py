from sqlalchemy import select
from sqlalchemy.orm import Session

from app.dominio.lugar import Lugar, TipoDeLugar
from app.infraestrutura.modelos import LugarORM


class LugarNaoEncontrado(LookupError):
    pass


def listar_lugares(sessao: Session, bairro: str | None = None,
                   tipo: TipoDeLugar | None = None) -> list[LugarORM]:
    consulta = select(LugarORM).order_by(LugarORM.nome)
    if bairro:
        consulta = consulta.where(LugarORM.bairro == bairro.strip())
    if tipo:
        consulta = consulta.where(LugarORM.tipo == tipo.value)
    return list(sessao.scalars(consulta))


def buscar_lugar(sessao: Session, lugar_id: int) -> LugarORM:
    lugar = sessao.get(LugarORM, lugar_id)
    if lugar is None:
        raise LugarNaoEncontrado(f"lugar {lugar_id} não encontrado")
    return lugar


def criar_lugar(sessao: Session, lugar: Lugar) -> LugarORM:
    orm = LugarORM(nome=lugar.nome, tipo=lugar.tipo.value,
                   bairro=lugar.bairro, como_e=lugar.como_e)
    sessao.add(orm)
    sessao.commit()
    sessao.refresh(orm)
    return orm


def atualizar_lugar(sessao: Session, lugar_id: int, lugar: Lugar) -> LugarORM:
    orm = buscar_lugar(sessao, lugar_id)
    orm.nome = lugar.nome
    orm.tipo = lugar.tipo.value
    orm.bairro = lugar.bairro
    orm.como_e = lugar.como_e
    sessao.commit()
    sessao.refresh(orm)
    return orm


def remover_lugar(sessao: Session, lugar_id: int) -> None:
    sessao.delete(buscar_lugar(sessao, lugar_id))
    sessao.commit()