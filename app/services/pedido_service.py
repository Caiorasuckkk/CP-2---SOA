from sqlalchemy.orm import Session

from app.models.pedido_model import Pedido, PedidoItem, StatusPedido
from app.repositories.pedido_repository import PedidoRepository
from app.repositories.cliente_repository import ClienteRepository
from app.services.estoque_service import EstoqueService
from app.services.pagamento_service import PagamentoService
from app.services.notificacao_service import NotificacaoService
from app.exceptions.exceptions import (
    PedidoNaoEncontradoException,
    ClienteNaoEncontradoException,
    PedidoSemItensException,
    TransicaoStatusInvalidaException,
    PagamentoRecusadoException,
)
from app.schemas.schemas import CriarPedidoRequest

TRANSICOES_VALIDAS: dict[str, list[str]] = {
    StatusPedido.CRIADO: [StatusPedido.AGUARDANDO_PAGAMENTO, StatusPedido.CANCELADO],
    StatusPedido.AGUARDANDO_PAGAMENTO: [StatusPedido.PAGO, StatusPedido.CANCELADO],
    StatusPedido.PAGO: [StatusPedido.FINALIZADO, StatusPedido.CANCELADO],
    StatusPedido.FINALIZADO: [],
    StatusPedido.CANCELADO: [],
}

class PedidoService:

    def __init__(self, db: Session):
        self.db = db
        self.repo = PedidoRepository(db)
        self.cliente_repo = ClienteRepository(db)
        self.estoque_service = EstoqueService(db)
        self.pagamento_service = PagamentoService(db)
        self.notificacao_service = NotificacaoService(db)

    def criar_pedido(self, dados: CriarPedidoRequest) -> Pedido:
        if not dados.itens:
            raise PedidoSemItensException()

        cliente = self.cliente_repo.buscar_por_id(dados.cliente_id)
        if not cliente:
            raise ClienteNaoEncontradoException(dados.cliente_id)

        produtos_validados = []
        for item in dados.itens:
            produto = self.estoque_service.verificar_disponibilidade(item.produto_id, item.quantidade)
            produtos_validados.append((item, produto))

        pedido = Pedido(
            cliente_id=dados.cliente_id,
            valor_total=0,
            status=StatusPedido.CRIADO,
        )
        self.repo.salvar(pedido)

        valor_total = 0.0
        for item_req, produto in produtos_validados:
            subtotal = float(produto.preco) * item_req.quantidade
            valor_total += subtotal

            pedido_item = PedidoItem(
                pedido_id=pedido.id,
                produto_id=produto.id,
                quantidade=item_req.quantidade,
                preco_unitario=produto.preco,
                subtotal=subtotal,
            )
            self.repo.adicionar_item(pedido_item)

        for item_req, produto in produtos_validados:
            self.estoque_service.reservar_estoque(produto.id, item_req.quantidade)

        self.repo.atualizar_valor_total(pedido, valor_total)
        self.repo.atualizar_status(pedido, StatusPedido.AGUARDANDO_PAGAMENTO)

        self.db.refresh(pedido)
        return pedido

    def processar_pagamento_pedido(self, pedido_id: int, forma_pagamento: str) -> Pedido:
        pedido = self._buscar_ou_404(pedido_id)

        try:
            self.pagamento_service.processar(pedido_id, forma_pagamento)
            self.repo.atualizar_status(pedido, StatusPedido.PAGO)
            self.notificacao_service.notificar_pagamento_aprovado(pedido_id)
            self.repo.atualizar_status(pedido, StatusPedido.FINALIZADO)
            self.notificacao_service.notificar_pedido_finalizado(pedido_id)

        except PagamentoRecusadoException as e:
            self._cancelar_e_repor_estoque(pedido, str(e))
            self.notificacao_service.notificar_pagamento_recusado(pedido_id)
            raise

        self.db.refresh(pedido)
        return pedido

    def buscar_por_id(self, pedido_id: int) -> Pedido:
        return self._buscar_ou_404(pedido_id)

    def listar_todos(self) -> list[Pedido]:
        return self.repo.listar_todos()

    def atualizar_status(self, pedido_id: int, novo_status: str) -> Pedido:
        pedido = self._buscar_ou_404(pedido_id)
        permitidos = TRANSICOES_VALIDAS.get(pedido.status, [])

        if novo_status not in permitidos:
            raise TransicaoStatusInvalidaException(pedido.status, novo_status)

        self.repo.atualizar_status(pedido, novo_status)

        if novo_status == StatusPedido.CANCELADO:
            self._cancelar_e_repor_estoque(pedido, "Cancelado manualmente.")

        self.db.refresh(pedido)
        return pedido

    def _buscar_ou_404(self, pedido_id: int) -> Pedido:
        pedido = self.repo.buscar_por_id(pedido_id)
        if not pedido:
            raise PedidoNaoEncontradoException(pedido_id)
        return pedido

    def _cancelar_e_repor_estoque(self, pedido: Pedido, motivo: str):
        for item in pedido.itens:
            self.estoque_service.repor_estoque(item.produto_id, item.quantidade)
        self.repo.atualizar_status(pedido, StatusPedido.CANCELADO)
        self.notificacao_service.notificar_pedido_cancelado(pedido.id, motivo)