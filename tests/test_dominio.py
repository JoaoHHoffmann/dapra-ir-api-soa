from datetime import date, datetime, timedelta, timezone

import pytest

from app.dominio.aviso import Aviso, Recurso
from app.dominio.erros import RegraViolada
from app.dominio.lugar import Lugar, TipoDeLugar
from app.dominio.plano import Veredito, montar_plano
from app.dominio.relato import Necessidade, Relato, Turno

AGORA = datetime(2026, 11, 10, 12, 0, tzinfo=timezone.utc)
ONTEM = date.today() - timedelta(days=1)


def aviso_elevador(inicio: datetime, valido_ate: datetime) -> Aviso:
    return Aviso(Recurso.ELEVADOR, "elevador parado", inicio, valido_ate)


def relato(turno: Turno, deu_certo: bool, necessidade=Necessidade.BARULHO) -> Relato:
    return Relato(ONTEM, turno, necessidade, deu_certo)


# --- Lugar ---

def test_lugar_remove_espacos_do_nome_e_do_bairro():
    lugar = Lugar("  UBS Vila Nova ", TipoDeLugar.UBS, " Vila Nova ")
    assert lugar.nome == "UBS Vila Nova"
    assert lugar.bairro == "Vila Nova"


def test_lugar_sem_nome_e_recusado():
    with pytest.raises(RegraViolada):
        Lugar("   ", TipoDeLugar.UBS, "Vila Nova")


# --- Aviso ---

def test_aviso_com_validade_antes_do_inicio_e_recusado():
    with pytest.raises(RegraViolada):
        aviso_elevador(AGORA, AGORA - timedelta(hours=1))


def test_aviso_esta_ativo_dentro_da_validade():
    aviso = aviso_elevador(AGORA - timedelta(days=1), AGORA + timedelta(days=1))
    assert aviso.esta_ativo(AGORA)


def test_aviso_vencido_nao_esta_ativo():
    aviso = aviso_elevador(AGORA - timedelta(days=2), AGORA - timedelta(days=1))
    assert not aviso.esta_ativo(AGORA)


# --- Relato ---

def test_relato_com_visita_no_futuro_e_recusado():
    with pytest.raises(RegraViolada):
        Relato(date.today() + timedelta(days=1), Turno.TARDE, Necessidade.BARULHO, True)


# --- Plano ---

def test_plano_sem_relatos():
    plano = montar_plano([], [], Necessidade.BARULHO, AGORA)
    assert plano.veredito == Veredito.SEM_RELATOS
    assert plano.melhor_turno is None


def test_plano_da_pra_ir_e_indica_o_melhor_turno():
    relatos = [relato(Turno.TARDE, True), relato(Turno.TARDE, True), relato(Turno.MANHA, False)]
    plano = montar_plano([], relatos, Necessidade.BARULHO, AGORA)
    assert plano.veredito == Veredito.DA_PRA_IR
    assert plano.melhor_turno == Turno.TARDE


def test_plano_com_aviso_ativo_vira_ressalva():
    aviso = aviso_elevador(AGORA - timedelta(days=1), AGORA + timedelta(days=1))
    plano = montar_plano([aviso], [relato(Turno.TARDE, True)], Necessidade.BARULHO, AGORA)
    assert plano.veredito == Veredito.DA_PRA_IR_COM_RESSALVAS
    assert plano.avisos_ativos == [aviso]


def test_plano_ignora_aviso_vencido():
    vencido = aviso_elevador(AGORA - timedelta(days=5), AGORA - timedelta(days=1))
    plano = montar_plano([vencido], [relato(Turno.TARDE, True)], Necessidade.BARULHO, AGORA)
    assert plano.veredito == Veredito.DA_PRA_IR
    assert plano.avisos_ativos == []


def test_plano_melhor_nao_ir_quando_a_maioria_nao_deu_certo():
    relatos = [relato(Turno.MANHA, False), relato(Turno.TARDE, False), relato(Turno.TARDE, True)]
    plano = montar_plano([], relatos, Necessidade.BARULHO, AGORA)
    assert plano.veredito == Veredito.MELHOR_NAO_IR


def test_plano_so_considera_relatos_da_necessidade_pedida():
    relatos = [relato(Turno.MANHA, False, Necessidade.CADEIRA_DE_RODAS)]
    plano = montar_plano([], relatos, Necessidade.BARULHO, AGORA)
    assert plano.veredito == Veredito.SEM_RELATOS