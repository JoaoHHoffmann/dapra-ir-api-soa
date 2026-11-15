from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.esquemas import NAO_ENCONTRADO, REGRA_VIOLADA, AvisoIn, AvisoOut
from app.aplicacao import avisos
from app.dominio.aviso import Aviso
from app.infraestrutura.db import get_session

router = APIRouter(prefix="/lugares/{lugar_id}/avisos", tags=["Avisos"])


@router.post("", response_model=AvisoOut, status_code=201,
             responses={**NAO_ENCONTRADO, **REGRA_VIOLADA},
             summary="Registra um aviso de hoje, como um elevador parado")
def registrar(lugar_id: int, dados: AvisoIn, sessao: Session = Depends(get_session)):
    aviso = Aviso(dados.recurso, dados.descricao, dados.inicio, dados.valido_ate)
    return avisos.registrar_aviso(sessao, lugar_id, aviso)


@router.get("", response_model=list[AvisoOut], responses=NAO_ENCONTRADO,
            summary="Lista os avisos de um lugar, do mais recente para o mais antigo")
def listar(lugar_id: int, sessao: Session = Depends(get_session)):
    return avisos.listar_avisos(sessao, lugar_id)