from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.schemas import ProdutoResponse, AtualizarEstoqueRequest, PagamentoResponse
from app.services.produto_service import ProdutoService
from app.services.estoque_service import EstoqueService
from app.services.pagamento_service import PagamentoService

router = APIRouter()

@router.get("/", response_model=list[ProdutoResponse])
def listar_produtos(db: Session = Depends(get_db)):
    return ProdutoService(db).listar_todos()

@router.get("/{produto_id}", response_model=ProdutoResponse)
def consultar_produto(produto_id: int, db: Session = Depends(get_db)):
    return ProdutoService(db).buscar_por_id(produto_id)