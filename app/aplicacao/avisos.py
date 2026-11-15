from sqlalchemy import select
from sqlalchemy.orm import Session

from app.aplicacao.lugares import buscar_lugar
from app.dominio.aviso import Aviso
from app.infraestrutura.modelos import AvisoORM


def registrar_aviso(sessao: Session, lugar_id: int, aviso: Aviso) -> AvisoORM:
    buscar_lugar(sessao, lugar_id)
    orm = AvisoORM(lugar_id=lugar_id, recurso=aviso.recurso.value, descricao=aviso.descricao,
                   inicio=aviso.inicio, valido_ate=aviso.valido_ate)
    sessao.add(orm)
    sessao.commit()
    sessao.refresh(orm)
    return orm


def listar_avisos(sessao: Session, lugar_id: int) -> list[AvisoORM]:
    buscar_lugar(sessao, lugar_id)
    consulta = (select(AvisoORM)
                .where(AvisoORM.lugar_id == lugar_id)
                .order_by(AvisoORM.inicio.desc()))
    return list(sessao.scalars(consulta))