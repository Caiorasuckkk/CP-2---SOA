import logging
from sqlalchemy.orm import Session
from app.models.notificacao_model import Notificacao, TipoNotificacao
from app.repositories.pagamento_repository import NotificacaoRepository

logger = logging.getLogger("notificacao")
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s - %(message)s")

class NotificacaoService:

    def __init__(self, db: Session):
        self.repo = NotificacaoRepository(db)

    def _registrar(self, pedido_id: int, tipo: str, mensagem: str) -> Notificacao:
        notificacao = Notificacao(pedido_id=pedido_id, tipo=tipo, mensagem=mensagem)
        salva = self.repo.salvar(notificacao)
        logger.info(f"[NOTIFICAÇÃO] Pedido #{pedido_id} | {tipo}: {mensagem}")
        return salva

    def notificar_pagamento_aprovado(self, pedido_id: int) -> Notificacao:
        return self._registrar(
            pedido_id,
            TipoNotificacao.PAGAMENTO_APROVADO,
            f"Pagamento do pedido #{pedido_id} foi aprovado com sucesso.",
        )

    def notificar_pagamento_recusado(self, pedido_id: int) -> Notificacao:
        return self._registrar(
            pedido_id,
            TipoNotificacao.PAGAMENTO_RECUSADO,
            f"Pagamento do pedido #{pedido_id} foi recusado. Tente novamente.",
        )

    def notificar_pedido_finalizado(self, pedido_id: int) -> Notificacao:
        return self._registrar(
            pedido_id,
            TipoNotificacao.PEDIDO_FINALIZADO,
            f"Pedido #{pedido_id} foi finalizado e está a caminho.",
        )

    def notificar_pedido_cancelado(self, pedido_id: int, motivo: str = "") -> Notificacao:
        msg = f"Pedido #{pedido_id} foi cancelado."
        if motivo:
            msg += f" Motivo: {motivo}"
        return self._registrar(pedido_id, TipoNotificacao.PEDIDO_CANCELADO, msg)

    def listar_por_pedido(self, pedido_id: int) -> list[Notificacao]:
        return self.repo.listar_por_pedido(pedido_id)