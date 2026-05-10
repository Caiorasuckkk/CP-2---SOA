from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class TipoNotificacao:
    PAGAMENTO_APROVADO = "PAGAMENTO_APROVADO"
    PEDIDO_FINALIZADO = "PEDIDO_FINALIZADO"
    PEDIDO_CANCELADO = "PEDIDO_CANCELADO"
    PAGAMENTO_RECUSADO = "PAGAMENTO_RECUSADO"

class Notificacao(Base):
    __tablename__ = "notificacoes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    tipo = Column(String(100), nullable=False)
    mensagem = Column(String(255), nullable=False)
    data_envio = Column(DateTime, server_default=func.now())

    pedido = relationship("Pedido", back_populates="notificacoes")