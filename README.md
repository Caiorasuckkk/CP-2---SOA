# 🛒 Sistema de Pedidos — CP2 FIAP 3ESPY 2026

> **Checkpoint 2 — Implementação da Arquitetura de Pedidos**  
> Disciplina: Arquitetura de Software | Profa. Damiana Costa

---

## 👥 Integrantes

| Nome | Turma |
|------|-------|
| _(preencher com nomes do grupo)_ | 3ESPY — 2026 |

---

## 📋 Descrição do Sistema

Sistema REST de gerenciamento de pedidos para uma plataforma de delivery, implementando os domínios de **Pedido**, **Produto**, **Estoque**, **Pagamento** e **Notificação**. O sistema valida regras de negócio, controla o fluxo de status dos pedidos e simula o processamento de pagamentos.

---

## 🛠 Tecnologias Utilizadas

| Tecnologia | Versão | Papel |
|---|---|---|
| **Python** | 3.12 | Linguagem principal |
| **FastAPI** | 0.115 | Framework web / REST API |
| **SQLAlchemy** | 2.0 | ORM / abstração do banco |
| **SQLite** | built-in | Persistência (dev/teste) |
| **Pydantic** | 2.9 | Validação de entrada e schemas |
| **Uvicorn** | 0.30 | Servidor ASGI |

> **Troca de banco:** basta alterar `DATABASE_URL` em `app/database.py` para PostgreSQL (`postgresql://user:pass@host/db`) sem mudar nenhum código de negócio.

---

## 🚀 Como Executar o Projeto

### Pré-requisitos
- Python 3.11 ou superior
- pip

### Instalação e execução

```bash
# 1. Clonar o repositório
git clone <url-do-repositorio>
cd sistema-pedidos

# 2. Criar e ativar ambiente virtual
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Executar a aplicação
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

A API estará disponível em: **http://localhost:8000**  
Documentação interativa (Swagger): **http://localhost:8000/docs**

> O banco SQLite é criado e populado automaticamente na primeira inicialização com 3 clientes e 4 produtos de exemplo.

---

## 📡 Lista de Endpoints

### 🧾 Pedidos

| Método | Endpoint | Descrição | Status de sucesso |
|--------|----------|-----------|-------------------|
| `POST` | `/pedidos/` | Cria um novo pedido | `201 Created` |
| `GET` | `/pedidos/` | Lista todos os pedidos | `200 OK` |
| `GET` | `/pedidos/{id}` | Consulta um pedido pelo ID | `200 OK` |
| `PUT` | `/pedidos/{id}/status` | Atualiza o status do pedido | `200 OK` |
| `POST` | `/pedidos/{id}/pagamento` | Processa o pagamento do pedido | `200 OK` |
| `GET` | `/pedidos/{id}/notificacoes` | Lista notificações do pedido | `200 OK` |
| `DELETE` | `/pedidos/{id}` | Cancela um pedido | `204 No Content` |

### 📦 Produtos

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/produtos/` | Lista todos os produtos |
| `GET` | `/produtos/{id}` | Consulta produto pelo ID |

### 📊 Estoque

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/estoque/{produto_id}` | Consulta estoque de um produto |
| `POST` | `/estoque/adicionar` | Adiciona unidades ao estoque |

### 💳 Pagamentos

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/pagamentos/{pedido_id}` | Lista pagamentos de um pedido |

---

### Exemplos de requisições

**Criar pedido:**
```json
POST /pedidos/
{
  "cliente_id": 1,
  "itens": [
    { "produto_id": 1, "quantidade": 2 },
    { "produto_id": 3, "quantidade": 1 }
  ]
}
```

**Processar pagamento:**
```json
POST /pedidos/1/pagamento
{
  "pedido_id": 1,
  "forma_pagamento": "PIX"
}
```
> Para simular **recusa**, use `"CARTAO_INVALIDO"` ou `"CREDITO_INSUFICIENTE"` como forma de pagamento.

**Atualizar status:**
```json
PUT /pedidos/1/status
{
  "status": "CANCELADO"
}
```

---

## 🏗 Explicação da Arquitetura

O sistema foi desenvolvido seguindo a **Arquitetura em Camadas** (Layered Architecture), com separação clara de responsabilidades entre quatro camadas principais:

```
┌─────────────────────────────────────────────────┐
│              CAMADA DE APRESENTAÇÃO              │
│         Controllers (FastAPI Routers)            │
│   Recebe HTTP → valida entrada → chama Service   │
├─────────────────────────────────────────────────┤
│              CAMADA DE NEGÓCIO                   │
│              Services (domínio)                  │
│  Orquestra regras de negócio, fluxos e eventos   │
├─────────────────────────────────────────────────┤
│              CAMADA DE DADOS                     │
│         Repositories (acesso ao banco)           │
│     Abstrai queries SQL via SQLAlchemy ORM       │
├─────────────────────────────────────────────────┤
│              CAMADA DE PERSISTÊNCIA              │
│       Models (SQLAlchemy) + SQLite/PostgreSQL    │
└─────────────────────────────────────────────────┘
```

### Descrição de cada camada

**Controllers:** recebem as requisições HTTP, extraem parâmetros, delegam ao service e retornam respostas com status HTTP corretos. Não contêm nenhuma regra de negócio.

**Services:** onde toda a lógica de negócio reside. Cada domínio possui seu próprio service (`PedidoService`, `PagamentoService`, `EstoqueService`, `NotificacaoService`), evitando classes "Deus" que concentram tudo.

**Repositories:** isolam o acesso ao banco de dados. Se o banco for trocado (ex: de SQLite para PostgreSQL), apenas esta camada precisa de ajuste.

**Models:** definem a estrutura das tabelas via ORM. Separados dos Schemas Pydantic (que definem o contrato da API), evitando acoplamento entre representação interna e representação externa.

---

## 🔀 Como as Responsabilidades foram Separadas

Cada domínio possui sua própria responsabilidade isolada:

| Componente | Responsabilidade exclusiva |
|---|---|
| `PedidoService` | Orquestra o fluxo do pedido, valida regras de status |
| `EstoqueService` | Verifica disponibilidade e gerencia quantidades |
| `PagamentoService` | Simula processamento e registra resultado |
| `NotificacaoService` | Registra eventos no banco e no log do sistema |
| `ProdutoService` | Consulta e expõe dados de produtos |
| `*Repository` | Abstrai o acesso ao banco de dados |
| `*Controller` | Traduz HTTP ↔ domínio |
| `exceptions/` | Centraliza erros de negócio mapeados para HTTP |
| `schemas/` | Define o contrato da API (entrada/saída) |

---

## ❓ Perguntas Discursivas

### 1. Como a comunicação entre os componentes do sistema foi organizada no código?

A comunicação entre os componentes foi organizada por meio de **injeção de dependência** e **orquestração centralizada no `PedidoService`**, sem que nenhum componente conheça os detalhes internos do outro.

Cada domínio possui seu próprio service, que é instanciado com a sessão de banco de dados e encapsulado em seu repositório. O `PedidoService` é o único que conhece os demais services — e os aciona na sequência correta do fluxo —, mas nunca acessa seus repositórios diretamente. Isso garante **baixo acoplamento**: o `PedidoService` sabe *o que* cada componente faz, mas não *como* ele faz.

Por exemplo, ao criar um pedido:
- `EstoqueService` é chamado para verificar disponibilidade — sem que `PedidoService` saiba como o banco de estoque funciona.
- `PagamentoService` é chamado para processar o pagamento — sem que `PedidoService` conheça a lógica de aprovação/recusa.
- `NotificacaoService` é chamado ao final — sem que os outros componentes saibam como a notificação é registrada.

Cada service é **coeso** (faz apenas o que lhe pertence) e **desacoplado** (não depende da implementação dos outros). Isso torna o sistema fácil de testar, modificar e escalar.

---

### 2. Se o componente de pagamento ficasse indisponível em um cenário real, qual seria o impacto na sua arquitetura? Como sua solução poderia evoluir para reduzir esse impacto?

**Impacto atual:** Na arquitetura atual, o `PagamentoService` é chamado de forma **síncrona** dentro do fluxo do pedido. Se o serviço de pagamento (ex: gateway externo) ficasse indisponível, a requisição falharia com erro 500, o pedido ficaria em estado `AGUARDANDO_PAGAMENTO` e o estoque já teria sido reservado — gerando inconsistência.

**Como a solução poderia evoluir:**

A principal evolução seria a adoção de um **padrão assíncrono com filas de mensagens (Message Broker)**, como RabbitMQ ou Apache Kafka:

1. Ao criar o pedido, em vez de chamar o pagamento diretamente, um **evento** seria publicado em uma fila (`pedido.aguardando_pagamento`).
2. Um **consumidor** do serviço de pagamento processaria esse evento de forma independente.
3. O resultado (aprovado/recusado) seria publicado em outro evento (`pagamento.resultado`), que o serviço de pedidos consumiria para atualizar o status.

Com isso:
- A criação do pedido não bloqueia esperando o pagamento.
- Se o serviço de pagamento cair, os eventos ficam na fila e são processados quando ele voltar — sem perda de dados.
- Os serviços ficam completamente desacoplados e podem escalar de forma independente.

Complementarmente, poderiam ser adotados:
- **Circuit Breaker** (ex: Resilience4j/tenacity) para detectar falhas e evitar cascata.
- **Retry com backoff exponencial** para tentativas automáticas.
- **Timeout configurado** para não deixar requisições presas indefinidamente.
- **Saga Pattern** para coordenar transações distribuídas com compensação automática (ex: repor estoque se pagamento falhar após timeout).

---

## 📊 Diagrama Arquitetural

Ver arquivo `diagrama_arquitetural.md` na raiz do repositório.

---

## 🗂 Estrutura do Projeto

```
sistema-pedidos/
├── app/
│   ├── main.py                    # Entry point da aplicação
│   ├── database.py                # Configuração do banco e seed
│   ├── controllers/               # Camada HTTP (routers FastAPI)
│   │   ├── pedido_controller.py
│   │   ├── produto_controller.py
│   │   ├── estoque_controller.py
│   │   └── pagamento_controller.py
│   ├── services/                  # Camada de negócio
│   │   ├── pedido_service.py
│   │   ├── pagamento_service.py
│   │   ├── estoque_service.py
│   │   ├── produto_service.py
│   │   └── notificacao_service.py
│   ├── repositories/              # Camada de acesso a dados
│   │   ├── pedido_repository.py
│   │   ├── produto_repository.py
│   │   ├── pagamento_repository.py
│   │   └── cliente_repository.py
│   ├── models/                    # Modelos ORM (tabelas)
│   │   ├── pedido_model.py
│   │   ├── produto_model.py
│   │   ├── cliente_model.py
│   │   ├── pagamento_model.py
│   │   └── notificacao_model.py
│   ├── schemas/                   # Contrato da API (Pydantic)
│   │   └── schemas.py
│   └── exceptions/                # Exceções de domínio e handlers
│       ├── exceptions.py
│       └── handlers.py
├── requirements.txt
└── README.md
```
