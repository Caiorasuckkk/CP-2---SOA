
class PedidoNaoEncontradoException(Exception):
    def __init__(self, pedido_id: int):
        self.pedido_id = pedido_id
        super().__init__(f"Pedido com id {pedido_id} não encontrado.")

class ProdutoNaoEncontradoException(Exception):
    def __init__(self, produto_id: int):
        self.produto_id = produto_id
        super().__init__(f"Produto com id {produto_id} não encontrado.")

class ClienteNaoEncontradoException(Exception):
    def __init__(self, cliente_id: int):
        self.cliente_id = cliente_id
        super().__init__(f"Cliente com id {cliente_id} não encontrado.")

class EstoqueInsuficienteException(Exception):
    def __init__(self, produto_nome: str, disponivel: int, solicitado: int):
        self.produto_nome = produto_nome
        self.disponivel = disponivel
        self.solicitado = solicitado
        super().__init__(
            f"Estoque insuficiente para '{produto_nome}': "
            f"disponível={disponivel}, solicitado={solicitado}."
        )

class PagamentoRecusadoException(Exception):
    def __init__(self, motivo: str = "Pagamento recusado pela operadora."):
        self.motivo = motivo
        super().__init__(motivo)

class PedidoSemItensException(Exception):
    def __init__(self):
        super().__init__("O pedido deve conter ao menos um item.")

class TransicaoStatusInvalidaException(Exception):
    def __init__(self, atual: str, novo: str):
        super().__init__(
            f"Transição de status inválida: '{atual}' → '{novo}'."
        )