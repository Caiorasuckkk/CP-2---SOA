from sqlalchemy.orm import Session
from app.repositories.produto_repository import ProdutoRepository
from app.exceptions.exceptions import ProdutoNaoEncontradoException
from app.models.produto_model import Produto

class ProdutoService:

    def __init__(self, db: Session):
        self.repo = ProdutoRepository(db)

    def listar_todos(self) -> list[Produto]:
        return self.repo.listar_todos()

    def buscar_por_id(self, produto_id: int) -> Produto:
        produto = self.repo.buscar_por_id(produto_id)
        if not produto:
            raise ProdutoNaoEncontradoException(produto_id)
        return produto