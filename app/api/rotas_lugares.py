from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.esquemas import Erro, LugarIn, LugarOut
from app.aplicacao import lugares
from app.dominio.lugar import Lugar, TipoDeLugar
from app.infraestrutura.db import get_session

router = APIRouter(prefix="/lugares", tags=["Lugares"])

NAO_ENCONTRADO = {404: {"model": Erro, "description": "Lugar não encontrado"}}
REGRA_VIOLADA = {422: {"description": "Dados inválidos ou regra do domínio violada"}}


def _para_dominio(dados: LugarIn) -> Lugar:
    return Lugar(dados.nome, dados.tipo, dados.bairro, dados.como_e)


@router.get("", response_model=list[LugarOut],
            summary="Lista os lugares, com filtro opcional por bairro e tipo")
def listar(bairro: str | None = None, tipo: TipoDeLugar | None = None,
           sessao: Session = Depends(get_session)):
    return lugares.listar_lugares(sessao, bairro, tipo)


@router.get("/{lugar_id}", response_model=LugarOut, responses=NAO_ENCONTRADO,
            summary="Busca um lugar pelo id")
def buscar(lugar_id: int, sessao: Session = Depends(get_session)):
    return lugares.buscar_lugar(sessao, lugar_id)


@router.post("", response_model=LugarOut, status_code=201, responses=REGRA_VIOLADA,
             summary="Cadastra um lugar")
def criar(dados: LugarIn, sessao: Session = Depends(get_session)):
    return lugares.criar_lugar(sessao, _para_dominio(dados))


@router.put("/{lugar_id}", response_model=LugarOut,
            responses={**NAO_ENCONTRADO, **REGRA_VIOLADA},
            summary="Atualiza um lugar")
def atualizar(lugar_id: int, dados: LugarIn, sessao: Session = Depends(get_session)):
    return lugares.atualizar_lugar(sessao, lugar_id, _para_dominio(dados))


@router.delete("/{lugar_id}", status_code=204, responses=NAO_ENCONTRADO,
               summary="Remove um lugar junto com seus avisos e relatos")
def remover(lugar_id: int, sessao: Session = Depends(get_session)):
    lugares.remover_lugar(sessao, lugar_id)