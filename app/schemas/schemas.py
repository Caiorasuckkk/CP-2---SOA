from pydantic import BaseModel, Field
from typing import List, Optional
from decimal import Decimal
from datetime import datetime

class ProdutoResponse(BaseModel):
    id: int
    nome: str
    descricao: Optional[str]
    preco: Decimal
    quantidade_estoque: int

    model_config = {"from_attributes": True}

class AtualizarEstoqueRequest(BaseModel):
    produto_id: int
    quantidade: int = Field(..., gt=0, description="Quantidade a adicionar ao estoque")

class ItemPedidoRequest(BaseModel):
    produto_id: int = Field(..., description="ID do produto")
    quantidade: int = Field(..., gt=0, description="Quantidade desejada")

class ItemPedidoResponse(BaseModel):
    id: int
    produto_id: int
    quantidade: int
    preco_unitario: Decimal
    subtotal: Decimal

    model_config = {"from_attributes": True}

class CriarPedidoRequest(BaseModel):
    cliente_id: int = Field(..., description="ID do cliente")
    itens: List[ItemPedidoRequest] = Field(..., min_length=1, description="Lista de itens (mínimo 1)")

class AtualizarStatusRequest(BaseModel):
    status: str = Field(..., description="Novo status do pedido")

class PedidoResponse(BaseModel):
    id: int
    cliente_id: int
    valor_total: Decimal
    status: str
    data_criacao: Optional[datetime]
    itens: List[ItemPedidoResponse] = []

    model_config = {"from_attributes": True}

class ProcessarPagamentoRequest(BaseModel):
    pedido_id: int
    forma_pagamento: str = Field(..., description="Ex: CARTAO_CREDITO, PIX, BOLETO")

class PagamentoResponse(BaseModel):
    id: int
    pedido_id: int
    valor: Decimal
    status: str
    forma_pagamento: Optional[str]
    data_pagamento: Optional[datetime]

    model_config = {"from_attributes": True}

class NotificacaoResponse(BaseModel):
    id: int
    pedido_id: int
    tipo: str
    mensagem: str
    data_envio: Optional[datetime]

    model_config = {"from_attributes": True}