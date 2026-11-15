from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.esquemas import NAO_ENCONTRADO, REGRA_VIOLADA, PlanoOut
from app.aplicacao import planos
from app.dominio.relato import Necessidade
from app.infraestrutura.db import get_session

router = APIRouter(prefix="/lugares/{lugar_id}/plano", tags=["Plano"])


@router.get("", response_model=PlanoOut, responses={**NAO_ENCONTRADO, **REGRA_VIOLADA},
            summary="Responde se dá pra ir ao lugar, considerando a necessidade da pessoa",
            description="Cruza os avisos ativos com os relatos de quem tem a mesma necessidade "
                        "e indica o veredito e o melhor turno para ir.")
def consultar(lugar_id: int, necessidade: Necessidade, sessao: Session = Depends(get_session)):
    return planos.consultar_plano(sessao, lugar_id, necessidade, datetime.now(timezone.utc))