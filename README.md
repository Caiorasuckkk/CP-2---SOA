# Sistema de Pedidos - CP2 FIAP



---

## Integrantes

| Nome | RM | Turma |
|------|----|-------|
| Caio Rasuck Barbosa | 93645 | 3ESPY 2026 |
| Arthur Menezes | 56296 | 3ESPY 2026 |

---

## Sobre o projeto

A ideia era pegar a arquitetura que a gente tinha desenhado no CP1 e colocar em código de verdade. Fizemos uma API REST de pedidos com os domínios de Pedido, Produto, Estoque, Pagamento e Notificação.

Usamos Python com FastAPI porque já tinhamos familiaridade e a documentação automática via Swagger ajuda bastante na hora de testar.

---

## Tecnologias

- Python 3.11
- FastAPI
- SQLAlchemy (ORM)
- SQLite (banco local, fácil de rodar sem configurar nada)
- Pydantic (validação)
- Uvicorn (servidor)

---

## Como rodar

```bash
git clone <url-do-repositorio>
cd sistema-pedidos

python -m venv venv
venv\Scripts\Activate.ps1   # Windows
# ou
source venv/bin/activate    # Linux/Mac

pip install -r requirements.txt

python -m uvicorn app.main:app --reload
```

Acessa em http://localhost:8000/docs — lá já tem a interface pra testar tudo.

O banco cria sozinho na primeira vez que roda, já com 3 clientes e 4 produtos de exemplo.

---

## Endpoints

### Pedidos

| Método | Rota | O que faz |
|--------|------|-----------|
| POST | /pedidos/ | Cria um pedido |
| GET | /pedidos/ | Lista todos |
| GET | /pedidos/{id} | Busca um pedido |
| PUT | /pedidos/{id}/status | Atualiza status |
| POST | /pedidos/{id}/pagamento | Processa pagamento |
| GET | /pedidos/{id}/notificacoes | Ver notificações |
| DELETE | /pedidos/{id} | Cancela o pedido |

### Produtos

| Método | Rota | O que faz |
|--------|------|-----------|
| GET | /produtos/ | Lista produtos |
| GET | /produtos/{id} | Busca produto |

### Estoque

| Método | Rota | O que faz |
|--------|------|-----------|
| GET | /estoque/{produto_id} | Consulta estoque |
| POST | /estoque/adicionar | Adiciona estoque |

### Pagamentos

| Método | Rota | O que faz |
|--------|------|-----------|
| GET | /pagamentos/{pedido_id} | Histórico de pagamentos |

### Exemplo rápido

Criar pedido:
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

Pagar:
```json
POST /pedidos/1/pagamento
{
  "pedido_id": 1,
  "forma_pagamento": "PIX"
}
```

Pra simular pagamento recusado, usa `"CARTAO_INVALIDO"` como forma de pagamento.

---

## Arquitetura

Seguimos a arquitetura em camadas, dividida assim:

```
Controller  →  Service  →  Repository  →  Banco
```

**Controller** só recebe a requisição HTTP e repassa pro service. Não tem nenhuma regra de negócio aqui.

**Service** é onde fica a lógica de verdade — validações, fluxo de status, orquestração entre os domínios.

**Repository** cuida do banco. Se um dia quiser trocar o SQLite por PostgreSQL, só muda aqui.

**Models** definem as tabelas. Os Schemas Pydantic ficam separados e servem como contrato da API.

Fluxo de status do pedido:
```
CRIADO → AGUARDANDO_PAGAMENTO → PAGO → FINALIZADO
                                    ↘ CANCELADO
```

---

## Estrutura de pastas

```
sistema-pedidos/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── controllers/
│   ├── services/
│   ├── repositories/
│   ├── models/
│   ├── schemas/
│   └── exceptions/
├── requirements.txt
└── README.md
```

---

## Perguntas discursivas

### 1. Como a comunicação entre os componentes foi organizada?

A gente tentou deixar cada parte do sistema responsável por uma coisa só. O `PedidoService` é quem coordena o fluxo quando um pedido é criado — ele chama o `EstoqueService` pra ver se tem produto disponível, depois o `PagamentoService` pra processar o pagamento, e por fim o `NotificacaoService` pra registrar o que aconteceu.

O que a gente quis evitar foi aquele negócio de colocar tudo num lugar só. Se o `PedidoService` precisasse saber como o banco de estoque funciona por dentro, qualquer mudança no estoque poderia quebrar o pedido. Então cada service cuida do seu domínio e expõe só o que o outro precisa saber.

O controller também não tem nada de lógica — ele recebe o JSON, passa pro service e devolve a resposta. Se precisar mudar alguma regra de negócio, a gente mexe só no service e não precisa tocar no resto.

### 2. Se o pagamento ficasse indisponível, qual seria o impacto e como evoluir?

Do jeito que tá hoje o pagamento é chamado direto, de forma síncrona. Se o serviço de pagamento cair no meio do fluxo, a requisição falha e o pedido pode ficar travado em `AGUARDANDO_PAGAMENTO` com o estoque já reservado — o que é um problema.

Pra resolver isso num cenário real, a gente usaria uma fila de mensagens tipo RabbitMQ ou Kafka. Em vez de chamar o pagamento diretamente, o sistema publicaria um evento na fila e o serviço de pagamento processaria quando pudesse. Se ele cair, os eventos ficam esperando na fila e são processados quando voltar — sem perder nada.

Outras coisas que ajudariam: um Circuit Breaker pra detectar quando o serviço tá fora e parar de tentar, retry automático com um tempo de espera entre as tentativas, e o padrão Saga pra conseguir desfazer operações caso algo dê errado no meio do caminho (tipo repor o estoque automaticamente se o pagamento não sair).
