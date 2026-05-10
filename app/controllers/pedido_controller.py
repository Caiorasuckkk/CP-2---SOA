from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.schemas import (
    CriarPedidoRequest,
    PedidoResponse,
    AtualizarStatusRequest,
    ProcessarPagamentoRequest,
    PagamentoResponse,
    NotificacaoResponse,
)
from app.services.pedido_service import PedidoService
from app.services.notificacao_service import NotificacaoService

router = APIRouter()

@router.post("/", response_model=PedidoResponse, status_code=status.HTTP_201_CREATED)
def criar_pedido(dados: CriarPedidoRequest, db: Session = Depends(get_db)):
    service = PedidoService(db)
    return service.criar_pedido(dados)

@router.get("/", response_model=list[PedidoResponse])
def listar_pedidos(db: Session = Depends(get_db)):
    return PedidoService(db).listar_todos()

@router.get("/{pedido_id}", response_model=PedidoResponse)
def consultar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    return PedidoService(db).buscar_por_id(pedido_id)

@router.put("/{pedido_id}/status", response_model=PedidoResponse)
def atualizar_status(pedido_id: int, dados: AtualizarStatusRequest, db: Session = Depends(get_db)):
    return PedidoService(db).atualizar_status(pedido_id, dados.status)

@router.post("/{pedido_id}/pagamento", response_model=PedidoResponse)
def processar_pagamento(pedido_id: int, dados: ProcessarPagamentoRequest, db: Session = Depends(get_db)):
    return PedidoService(db).processar_pagamento_pedido(pedido_id, dados.forma_pagamento)

@router.get("/{pedido_id}/notificacoes", response_model=list[NotificacaoResponse])
def listar_notificacoes(pedido_id: int, db: Session = Depends(get_db)):
    return NotificacaoService(db).listar_por_pedido(pedido_id)

@router.delete("/{pedido_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancelar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    PedidoService(db).atualizar_status(pedido_id, "CANCELADO")