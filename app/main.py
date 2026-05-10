from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers import pedido_controller, produto_controller, estoque_controller, pagamento_controller
from app.exceptions.handlers import register_exception_handlers
from app.database import init_db

app = FastAPI(
    title="Sistema de Pedidos - CP2 FIAP",
    description="API REST para gerenciamento de pedidos com arquitetura em camadas",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)

app.include_router(pedido_controller.router, prefix="/pedidos", tags=["Pedidos"])
app.include_router(produto_controller.router, prefix="/produtos", tags=["Produtos"])
app.include_router(estoque_controller.router, prefix="/estoque", tags=["Estoque"])
app.include_router(pagamento_controller.router, prefix="/pagamentos", tags=["Pagamentos"])

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "sistema": "Sistema de Pedidos CP2 - FIAP"}