import random
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.pagamento_model import Pagamento, StatusPagamento
from app.repositories.pagamento_repository import PagamentoRepository
from app.exceptions.exceptions import PagamentoRecusadoException, PedidoNaoEncontradoException
from app.repositories.pedido_repository import PedidoRepository

FORMAS_RECUSADAS = {"CARTAO_INVALIDO", "CREDITO_INSUFICIENTE"}

class PagamentoService:

    def __init__(self, db: Session):
        self.repo = PagamentoRepository(db)
        self.pedido_repo = PedidoRepository(db)

    def processar(self, pedido_id: int, forma_pagamento: str) -> Pagamento:
        pedido = self.pedido_repo.buscar_por_id(pedido_id)
        if not pedido:
            raise PedidoNaoEncontradoException(pedido_id)

        pagamento = Pagamento(
            pedido_id=pedido_id,
            valor=pedido.valor_total,
            forma_pagamento=forma_pagamento.upper(),
            status=StatusPagamento.PENDENTE,
        )
        self.repo.salvar(pagamento)

        aprovado = forma_pagamento.upper() not in FORMAS_RECUSADAS

        if aprovado:
            pagamento.status = StatusPagamento.APROVADO
            pagamento.data_pagamento = datetime.now()
            self.repo.atualizar(pagamento)
            return pagamento
        else:
            pagamento.status = StatusPagamento.RECUSADO
            self.repo.atualizar(pagamento)
            raise PagamentoRecusadoException(
                f"Pagamento recusado para a forma '{forma_pagamento}'. "
                "Verifique os dados do cartão ou tente outra forma de pagamento."
            )

    def consultar_por_pedido(self, pedido_id: int) -> list[Pagamento]:
        return self.repo.buscar_por_pedido(pedido_id)