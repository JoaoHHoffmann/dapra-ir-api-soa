import os

os.environ.setdefault("DATABASE_URL", "sqlite://") 

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.infraestrutura.db import Base, get_session
from app.infraestrutura.modelos import LugarORM
from main import app

ONTEM = "2026-11-01"


@pytest.fixture
def cliente():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False},
                           poolclass=StaticPool)
    Base.metadata.create_all(engine)
    SessaoDeTeste = sessionmaker(bind=engine)

    with SessaoDeTeste() as sessao:
        sessao.add(LugarORM(nome="UBS Teste", tipo="UBS", bairro="Centro"))
        sessao.commit()

    def sessao_de_teste():
        with SessaoDeTeste() as sessao:
            yield sessao

    app.dependency_overrides[get_session] = sessao_de_teste
    yield TestClient(app)
    app.dependency_overrides.clear()


def relato(turno: str, deu_certo: bool) -> dict:
    return {"data_visita": ONTEM, "turno": turno, "necessidade": "BARULHO", "deu_certo": deu_certo}


def test_cria_lugar_e_responde_201(cliente):
    r = cliente.post("/lugares", json={"nome": " Escola Azul ", "tipo": "ESCOLA", "bairro": "Centro"})
    assert r.status_code == 201
    assert r.json()["nome"] == "Escola Azul"
    assert r.json()["tipo"] == "ESCOLA"


def test_lista_lugares_filtrando_por_tipo(cliente):
    cliente.post("/lugares", json={"nome": "Escola Azul", "tipo": "ESCOLA", "bairro": "Centro"})
    r = cliente.get("/lugares", params={"tipo": "UBS"})
    assert r.status_code == 200
    assert [l["nome"] for l in r.json()] == ["UBS Teste"]


def test_lugar_sem_nome_responde_422(cliente):
    r = cliente.post("/lugares", json={"nome": "   ", "tipo": "UBS", "bairro": "Centro"})
    assert r.status_code == 422
    assert r.json()["detail"] == "o lugar precisa ter um nome"


def test_lugar_inexistente_responde_404(cliente):
    r = cliente.get("/lugares/99")
    assert r.status_code == 404
    assert r.json()["detail"] == "lugar 99 não encontrado"


def test_atualiza_e_remove_lugar(cliente):
    r = cliente.put("/lugares/1", json={"nome": "UBS Nova", "tipo": "UBS", "bairro": "Centro"})
    assert r.status_code == 200
    assert r.json()["nome"] == "UBS Nova"

    assert cliente.delete("/lugares/1").status_code == 204
    assert cliente.get("/lugares/1").status_code == 404


def test_relato_com_visita_no_futuro_responde_422(cliente):
    r = cliente.post("/lugares/1/relatos", json={**relato("TARDE", True), "data_visita": "2099-01-01"})
    assert r.status_code == 422
    assert r.json()["detail"] == "a data da visita não pode estar no futuro"


def test_plano_indica_o_melhor_turno(cliente):
    for turno, deu_certo in [("TARDE", True), ("TARDE", True), ("MANHA", False)]:
        assert cliente.post("/lugares/1/relatos", json=relato(turno, deu_certo)).status_code == 201

    r = cliente.get("/lugares/1/plano", params={"necessidade": "BARULHO"})
    assert r.status_code == 200
    assert r.json() == {"veredito": "DA_PRA_IR", "melhor_turno": "TARDE", "avisos_ativos": []}