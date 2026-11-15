from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api import rotas_avisos, rotas_lugares, rotas_plano, rotas_relatos
from app.aplicacao.lugares import LugarNaoEncontrado
from app.dominio.erros import RegraViolada

app = FastAPI(
    title="Dá Pra Ir? · API",
    version="1.0.0",
    description="Backend da CitizenTech Dá Pra Ir?: lugares, avisos e relatos de acessibilidade.",
)

app.include_router(rotas_lugares.router)
app.include_router(rotas_avisos.router)
app.include_router(rotas_relatos.router)
app.include_router(rotas_plano.router)


@app.exception_handler(LugarNaoEncontrado)
def lugar_nao_encontrado(request: Request, erro: LugarNaoEncontrado):
    return JSONResponse(status_code=404, content={"detail": str(erro)})


@app.exception_handler(RegraViolada)
def regra_violada(request: Request, erro: RegraViolada):
    return JSONResponse(status_code=422, content={"detail": str(erro)})