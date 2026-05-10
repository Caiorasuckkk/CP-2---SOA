from sqlalchemy.orm import Session
from app.models.pedido_model import Pedido, PedidoItem

class PedidoRepository:

    def __init__(self, db: Session):
        self.db = db

    def buscar_por_id(self, pedido_id: int) -> Pedido | None:
        return self.db.query(Pedido).filter(Pedido.id == pedido_id).first()

    def listar_todos(self) -> list[Pedido]:
        return self.db.query(Pedido).all()

    def listar_por_cliente(self, cliente_id: int) -> list[Pedido]:
        return self.db.query(Pedido).filter(Pedido.cliente_id == cliente_id).all()

    def salvar(self, pedido: Pedido) -> Pedido:
        self.db.add(pedido)
        self.db.commit()
        self.db.refresh(pedido)
        return pedido

    def atualizar_status(self, pedido: Pedido, novo_status: str) -> Pedido:
        pedido.status = novo_status
        self.db.commit()
        self.db.refresh(pedido)
        return pedido

    def atualizar_valor_total(self, pedido: Pedido, valor: float) -> Pedido:
        pedido.valor_total = valor
        self.db.commit()
        self.db.refresh(pedido)
        return pedido

    def adicionar_item(self, item: PedidoItem) -> PedidoItem:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def deletar(self, pedido_id: int) -> bool:
        pedido = self.buscar_por_id(pedido_id)
        if pedido:
            self.db.delete(pedido)
            self.db.commit()
            return True
        return False