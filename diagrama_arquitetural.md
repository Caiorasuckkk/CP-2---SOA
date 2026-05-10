# Diagrama Arquitetural — Sistema de Pedidos CP2

## Arquitetura em Camadas

```
┌──────────────────────────────────────────────────────────────┐
│                     CLIENTE HTTP                             │
│              (Postman / Frontend / Curl)                     │
└─────────────────────────┬────────────────────────────────────┘
                          │ REST API (JSON)
                          ▼
┌──────────────────────────────────────────────────────────────┐
│              CAMADA DE APRESENTAÇÃO — Controllers            │
│  PedidoController  │  ProdutoController  │  EstoqueController│
│                    │  PagamentoController                    │
│  Responsabilidade: receber HTTP, validar entrada (Pydantic), │
│  delegar ao Service, retornar resposta com status correto    │
└─────────────────────────┬────────────────────────────────────┘
                          │ Chamada de método (injeção de dep.)
                          ▼
┌──────────────────────────────────────────────────────────────┐
│              CAMADA DE NEGÓCIO — Services                    │
│                                                              │
│  ┌────────────────┐  ┌───────────────┐  ┌────────────────┐  │
│  │ PedidoService  │→ │EstoqueService │  │PagamentoService│  │
│  │ (orquestrador) │  │verifica estq. │  │processa pag.   │  │
│  └───────┬────────┘  └───────────────┘  └────────────────┘  │
│          │                                                   │
│  ┌───────▼────────┐  ┌─────────────────────────────────┐    │
│  │ProdutoService  │  │    NotificacaoService           │    │
│  │consulta dados  │  │ registra eventos (log + banco)  │    │
│  └────────────────┘  └─────────────────────────────────┘    │
│                                                              │
│  Responsabilidade: toda regra de negócio, validações,        │
│  orquestração do fluxo de pedidos                            │
└─────────────────────────┬────────────────────────────────────┘
                          │ Chamadas ao ORM
                          ▼
┌──────────────────────────────────────────────────────────────┐
│              CAMADA DE DADOS — Repositories                  │
│  PedidoRepository  │  ProdutoRepository │  ClienteRepository │
│  PagamentoRepository   │   NotificacaoRepository             │
│                                                              │
│  Responsabilidade: abstração total do banco de dados.        │
│  Services não fazem queries diretamente.                     │
└─────────────────────────┬────────────────────────────────────┘
                          │ SQLAlchemy ORM
                          ▼
┌──────────────────────────────────────────────────────────────┐
│              CAMADA DE PERSISTÊNCIA — Models + Banco         │
│  clientes | produtos | pedidos | pedido_itens                │
│  pagamentos | notificacoes                                   │
│                                                              │
│  SQLite (desenvolvimento) → PostgreSQL (produção)            │
│  Troca: apenas DATABASE_URL em database.py                   │
└──────────────────────────────────────────────────────────────┘
```

## Fluxo de Criação de Pedido

```
Cliente → POST /pedidos
    │
    ▼
PedidoController
    │ CriarPedidoRequest (Pydantic valida)
    ▼
PedidoService.criar_pedido()
    ├─→ ClienteRepository.buscar_por_id()    [valida cliente]
    ├─→ EstoqueService.verificar_disponibilidade()  [para cada item]
    │       └─→ ProdutoRepository.buscar_por_id()
    ├─→ PedidoRepository.salvar()            [persiste pedido]
    ├─→ PedidoRepository.adicionar_item()    [persiste itens]
    ├─→ EstoqueService.reservar_estoque()    [reduz estoque]
    └─→ PedidoRepository.atualizar_status()  [AGUARDANDO_PAGAMENTO]
    │
    ▼
PedidoResponse (Pydantic serializa)
    │
    ▼
201 Created
```

## Fluxo de Pagamento

```
Cliente → POST /pedidos/{id}/pagamento
    │
    ▼
PedidoController
    │
    ▼
PedidoService.processar_pagamento_pedido()
    ├─→ PagamentoService.processar()
    │       ├─ [APROVADO] → salva Pagamento(status=APROVADO)
    │       └─ [RECUSADO] → salva Pagamento(status=RECUSADO)
    │                        └─→ raise PagamentoRecusadoException
    │
    ├─ [APROVADO]:
    │   ├─→ PedidoRepository.atualizar_status(PAGO)
    │   ├─→ NotificacaoService.notificar_pagamento_aprovado()
    │   ├─→ PedidoRepository.atualizar_status(FINALIZADO)
    │   └─→ NotificacaoService.notificar_pedido_finalizado()
    │
    └─ [RECUSADO]:
        ├─→ EstoqueService.repor_estoque()  [para cada item]
        ├─→ PedidoRepository.atualizar_status(CANCELADO)
        └─→ NotificacaoService.notificar_pedido_cancelado()
            └─→ NotificacaoService.notificar_pagamento_recusado()
```

## Transições de Status Permitidas

```
CRIADO ──────────────────────────────────────────────────────┐
   │                                                         │
   ▼                                                         │
AGUARDANDO_PAGAMENTO ─────────────────────────────────────── │ → CANCELADO
   │                                                         │
   ▼ (pagamento aprovado)                                    │
PAGO ──────────────────────────────────────────────────────── │
   │                                                         │
   ▼                                                         │
FINALIZADO (estado terminal)
```
