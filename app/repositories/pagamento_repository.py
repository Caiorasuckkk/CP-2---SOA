from sqlalchemy.orm import Session
from app.models.pagamento_model import Pagamento
from app.models.notificacao_model import Notificacao

class PagamentoRepository:

    def __init__(self, db: Session):
        self.db = db

    def buscar_por_id(self, pagamento_id: int) -> Pagamento | None:
        return self.db.query(Pagamento).filter(Pagamento.id == pagamento_id).first()

    def buscar_por_pedido(self, pedido_id: int) -> list[Pagamento]:
        return self.db.query(Pagamento).filter(Pagamento.pedido_id == pedido_id).all()

    def salvar(self, pagamento: Pagamento) -> Pagamento:
        self.db.add(pagamento)
        self.db.commit()
        self.db.refresh(pagamento)
        return pagamento

    def atualizar(self, pagamento: Pagamento) -> Pagamento:
        self.db.commit()
        self.db.refresh(pagamento)
        return pagamento

class NotificacaoRepository:

    def __init__(self, db: Session):
        self.db = db

    def salvar(self, notificacao: Notificacao) -> Notificacao:
        self.db.add(notificacao)
        self.db.commit()
        self.db.refresh(notificacao)
        return notificacao

    def listar_por_pedido(self, pedido_id: int) -> list[Notificacao]:
        return self.db.query(Notificacao).filter(Notificacao.pedido_id == pedido_id).all()