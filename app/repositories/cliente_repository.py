from sqlalchemy.orm import Session
from app.models.cliente_model import Cliente

class ClienteRepository:

    def __init__(self, db: Session):
        self.db = db

    def buscar_por_id(self, cliente_id: int) -> Cliente | None:
        return self.db.query(Cliente).filter(Cliente.id == cliente_id).first()

    def listar_todos(self) -> list[Cliente]:
        return self.db.query(Cliente).all()