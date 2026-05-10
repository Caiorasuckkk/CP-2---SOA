from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.schemas import AtualizarEstoqueRequest, ProdutoResponse
from app.services.estoque_service import EstoqueService

router = APIRouter()

@router.get("/{produto_id}")
def consultar_estoque(produto_id: int, db: Session = Depends(get_db)):
    return EstoqueService(db).consultar_estoque(produto_id)

@router.post("/adicionar", response_model=ProdutoResponse)
def adicionar_estoque(dados: AtualizarEstoqueRequest, db: Session = Depends(get_db)):
    return EstoqueService(db).adicionar_estoque(dados.produto_id, dados.quantidade)