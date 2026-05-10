from sqlalchemy import Column, Integer, Numeric, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class StatusPagamento:
    APROVADO = "APROVADO"
    RECUSADO = "RECUSADO"
    PENDENTE = "PENDENTE"

class Pagamento(Base):
    __tablename__ = "pagamentos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    valor = Column(Numeric(10, 2), nullable=False)
    status = Column(String(50), nullable=False, default=StatusPagamento.PENDENTE)
    forma_pagamento = Column(String(50))
    data_pagamento = Column(DateTime, nullable=True)

    pedido = relationship("Pedido", back_populates="pagamentos")