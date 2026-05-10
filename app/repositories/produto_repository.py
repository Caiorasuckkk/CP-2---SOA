from sqlalchemy.orm import Session
from app.models.produto_model import Produto

class ProdutoRepository:

    def __init__(self, db: Session):
        self.db = db

    def buscar_por_id(self, produto_id: int) -> Produto | None:
        return self.db.query(Produto).filter(Produto.id == produto_id).first()

    def listar_todos(self) -> list[Produto]:
        return self.db.query(Produto).all()

    def salvar(self, produto: Produto) -> Produto:
        self.db.add(produto)
        self.db.commit()
        self.db.refresh(produto)
        return produto

    def reduzir_estoque(self, produto_id: int, quantidade: int) -> Produto:
        produto = self.buscar_por_id(produto_id)
        produto.quantidade_estoque -= quantidade
        self.db.commit()
        self.db.refresh(produto)
        return produto

    def aumentar_estoque(self, produto_id: int, quantidade: int) -> Produto:
        produto = self.buscar_por_id(produto_id)
        produto.quantidade_estoque += quantidade
        self.db.commit()
        self.db.refresh(produto)
        return produto