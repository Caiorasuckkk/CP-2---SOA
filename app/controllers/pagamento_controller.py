from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.schemas import PagamentoResponse
from app.services.pagamento_service import PagamentoService

router = APIRouter()

@router.get("/{pedido_id}", response_model=list[PagamentoResponse])
def consultar_pagamentos_pedido(pedido_id: int, db: Session = Depends(get_db)):
    return PagamentoService(db).consultar_por_pedido(pedido_id)