from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.esquemas import NAO_ENCONTRADO, REGRA_VIOLADA, RelatoIn, RelatoOut
from app.aplicacao import relatos
from app.dominio.relato import Relato
from app.infraestrutura.db import get_session

router = APIRouter(prefix="/lugares/{lugar_id}/relatos", tags=["Relatos"])


@router.post("", response_model=RelatoOut, status_code=201,
             responses={**NAO_ENCONTRADO, **REGRA_VIOLADA},
             summary="Registra um relato anônimo de visita: deu certo ou não deu")
def registrar(lugar_id: int, dados: RelatoIn, sessao: Session = Depends(get_session)):
    relato = Relato(dados.data_visita, dados.turno, dados.necessidade,
                    dados.deu_certo, dados.comentario)
    return relatos.registrar_relato(sessao, lugar_id, relato)


@router.get("", response_model=list[RelatoOut], responses=NAO_ENCONTRADO,
            summary="Lista os relatos de um lugar, do mais recente para o mais antigo")
def listar(lugar_id: int, sessao: Session = Depends(get_session)):
    return relatos.listar_relatos(sessao, lugar_id)