from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions.exceptions import (
    PedidoNaoEncontradoException,
    ProdutoNaoEncontradoException,
    ClienteNaoEncontradoException,
    EstoqueInsuficienteException,
    PagamentoRecusadoException,
    PedidoSemItensException,
    TransicaoStatusInvalidaException,
)

def register_exception_handlers(app: FastAPI):

    @app.exception_handler(PedidoNaoEncontradoException)
    async def pedido_nao_encontrado(request: Request, exc: PedidoNaoEncontradoException):
        return JSONResponse(status_code=404, content={"erro": str(exc)})

    @app.exception_handler(ProdutoNaoEncontradoException)
    async def produto_nao_encontrado(request: Request, exc: ProdutoNaoEncontradoException):
        return JSONResponse(status_code=404, content={"erro": str(exc)})

    @app.exception_handler(ClienteNaoEncontradoException)
    async def cliente_nao_encontrado(request: Request, exc: ClienteNaoEncontradoException):
        return JSONResponse(status_code=404, content={"erro": str(exc)})

    @app.exception_handler(EstoqueInsuficienteException)
    async def estoque_insuficiente(request: Request, exc: EstoqueInsuficienteException):
        return JSONResponse(status_code=422, content={"erro": str(exc)})

    @app.exception_handler(PagamentoRecusadoException)
    async def pagamento_recusado(request: Request, exc: PagamentoRecusadoException):
        return JSONResponse(status_code=402, content={"erro": str(exc)})

    @app.exception_handler(PedidoSemItensException)
    async def pedido_sem_itens(request: Request, exc: PedidoSemItensException):
        return JSONResponse(status_code=400, content={"erro": str(exc)})

    @app.exception_handler(TransicaoStatusInvalidaException)
    async def status_invalido(request: Request, exc: TransicaoStatusInvalidaException):
        return JSONResponse(status_code=409, content={"erro": str(exc)})