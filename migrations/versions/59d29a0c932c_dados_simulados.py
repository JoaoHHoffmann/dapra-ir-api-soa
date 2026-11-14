"""dados simulados

Revision ID: 59d29a0c932c
Revises: 2e11cb9f0c46
Create Date: 2026-11-14 00:08:51.399373

"""
from typing import Sequence, Union
from datetime import date, datetime, timezone
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '59d29a0c932c'
down_revision: Union[str, Sequence[str], None] = '2e11cb9f0c46'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Dados simulados: lugares, avisos e relatos fictícios, criados pela equipe.
NOMES = ("UBS Jardim Esperança", "Estação Jardim Esperança", "Consultório Sorriso Azul")

LUGARES = [
    {"nome": NOMES[0], "tipo": "UBS", "bairro": "Jardim Esperança",
     "como_e": "Entrada principal com degraus; a entrada lateral tem rampa. "
               "De manhã a sala de espera fica cheia e barulhenta."},
    {"nome": NOMES[1], "tipo": "ESTACAO", "bairro": "Jardim Esperança",
     "como_e": "Elevador na saída B. Plataforma lotada entre 7h e 9h."},
    {"nome": NOMES[2], "tipo": "DENTISTA", "bairro": "Jardim Esperança",
     "como_e": "Atende crianças autistas; dá para pedir a última consulta da tarde."},
]


def upgrade() -> None:
    lugar = sa.table("lugar", sa.column("nome"), sa.column("tipo"),
                     sa.column("bairro"), sa.column("como_e"))
    op.bulk_insert(lugar, LUGARES)

    # busca os ids gerados pelo banco para ligar avisos e relatos ao lugar certo
    ids = dict(op.get_bind().execute(sa.text("SELECT nome, id FROM lugar")).all())
    ubs, estacao, dentista = (ids[nome] for nome in NOMES)

    aviso = sa.table("aviso", sa.column("lugar_id"), sa.column("recurso"),
                     sa.column("descricao"), sa.column("inicio", sa.DateTime(timezone=True)),
                     sa.column("valido_ate", sa.DateTime(timezone=True)))
    op.bulk_insert(aviso, [
        {"lugar_id": estacao, "recurso": "ELEVADOR", "descricao": "Elevador da saída B parado",
         "inicio": datetime(2026, 11, 1, 8, tzinfo=timezone.utc),
         "valido_ate": datetime(2027, 12, 31, 23, tzinfo=timezone.utc)},
        {"lugar_id": ubs, "recurso": "RAMPA", "descricao": "Rampa lateral em obra",
         "inicio": datetime(2026, 10, 1, 8, tzinfo=timezone.utc),
         "valido_ate": datetime(2026, 10, 15, 18, tzinfo=timezone.utc)},
    ])

    relato = sa.table("relato", sa.column("lugar_id"), sa.column("data_visita", sa.Date),
                      sa.column("turno"), sa.column("necessidade"),
                      sa.column("deu_certo", sa.Boolean), sa.column("comentario"))
    op.bulk_insert(relato, [
        {"lugar_id": ubs, "data_visita": date(2026, 10, 20), "turno": "MANHA",
         "necessidade": "BARULHO", "deu_certo": False, "comentario": "Sala de espera muito cheia."},
        {"lugar_id": ubs, "data_visita": date(2026, 10, 22), "turno": "TARDE",
         "necessidade": "BARULHO", "deu_certo": True, "comentario": "Tranquilo depois das 14h."},
        {"lugar_id": ubs, "data_visita": date(2026, 10, 27), "turno": "TARDE",
         "necessidade": "BARULHO", "deu_certo": True, "comentario": ""},
        {"lugar_id": estacao, "data_visita": date(2026, 11, 3), "turno": "MANHA",
         "necessidade": "CADEIRA_DE_RODAS", "deu_certo": False, "comentario": "Elevador parado."},
        {"lugar_id": dentista, "data_visita": date(2026, 10, 30), "turno": "TARDE",
         "necessidade": "BARULHO", "deu_certo": True, "comentario": "Atendimento sem pressa."},
    ])


def downgrade() -> None:
    nomes = ", ".join(f"'{nome}'" for nome in NOMES)
    op.execute(f"DELETE FROM relato WHERE lugar_id IN (SELECT id FROM lugar WHERE nome IN ({nomes}))")
    op.execute(f"DELETE FROM aviso WHERE lugar_id IN (SELECT id FROM lugar WHERE nome IN ({nomes}))")
    op.execute(f"DELETE FROM lugar WHERE nome IN ({nomes})")
