from sqlalchemy.orm import Session
from app.repositories.produto_repository import ProdutoRepository
from app.exceptions.exceptions import ProdutoNaoEncontradoException, EstoqueInsuficienteException
from app.models.produto_model import Produto

class EstoqueService:

    def __init__(self, db: Session):
        self.repo = ProdutoRepository(db)

    def verificar_disponibilidade(self, produto_id: int, quantidade: int) -> Produto:
        produto = self.repo.buscar_por_id(produto_id)
        if not produto:
            raise ProdutoNaoEncontradoException(produto_id)
        if produto.quantidade_estoque < quantidade:
            raise EstoqueInsuficienteException(produto.nome, produto.quantidade_estoque, quantidade)
        return produto

    def reservar_estoque(self, produto_id: int, quantidade: int) -> Produto:
        self.verificar_disponibilidade(produto_id, quantidade)
        return self.repo.reduzir_estoque(produto_id, quantidade)

    def repor_estoque(self, produto_id: int, quantidade: int) -> Produto:
        produto = self.repo.buscar_por_id(produto_id)
        if not produto:
            raise ProdutoNaoEncontradoException(produto_id)
        return self.repo.aumentar_estoque(produto_id, quantidade)

    def adicionar_estoque(self, produto_id: int, quantidade: int) -> Produto:
        produto = self.repo.buscar_por_id(produto_id)
        if not produto:
            raise ProdutoNaoEncontradoException(produto_id)
        return self.repo.aumentar_estoque(produto_id, quantidade)

    def consultar_estoque(self, produto_id: int) -> dict:
        produto = self.repo.buscar_por_id(produto_id)
        if not produto:
            raise ProdutoNaoEncontradoException(produto_id)
        return {"produto_id": produto_id, "nome": produto.nome, "quantidade_estoque": produto.quantidade_estoque}