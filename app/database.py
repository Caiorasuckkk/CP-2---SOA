from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "sqlite:///./pedidos.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    from app.models import cliente_model, produto_model, pedido_model, pagamento_model, notificacao_model
    Base.metadata.create_all(bind=engine)
    _seed_data()

def _seed_data():
    from app.models.cliente_model import Cliente
    from app.models.produto_model import Produto

    db = SessionLocal()
    try:
        if db.query(Cliente).count() > 0:
            return

        clientes = [
            Cliente(nome="Ana Souza", email="ana@email.com"),
            Cliente(nome="Bruno Lima", email="bruno@email.com"),
            Cliente(nome="Carla Mendes", email="carla@email.com"),
        ]
        db.add_all(clientes)

        produtos = [
            Produto(nome="Hambúrguer Artesanal", descricao="Pão, carne, queijo e molho especial", preco=32.90, quantidade_estoque=10),
            Produto(nome="Pizza Calabresa", descricao="Pizza média de calabresa", preco=49.90, quantidade_estoque=5),
            Produto(nome="Refrigerante 2L", descricao="Refrigerante cola 2 litros", preco=12.00, quantidade_estoque=20),
            Produto(nome="Batata Frita", descricao="Porção média de batata frita", preco=18.50, quantidade_estoque=8),
        ]
        db.add_all(produtos)
        db.commit()
    finally:
        db.close()