# 📡 Documentação da API - SaaS de Suporte ao Cliente

## URL Base
```
http://localhost:8000/api/v1
```

## Autenticação

Todos os endpoints (exceto registro e login) requerem autenticação via JWT Bearer Token.

**Header:**
```
Authorization: Bearer <seu_token_aqui>
```

---

## 🔐 Autenticação

### Registrar Usuário
**POST** `/auth/register`

**Body:**
```json
{
  "email": "usuario@email.com",
  "full_name": "Nome do Usuário",
  "password": "senha123456",
  "role": "customer"
}
```

**Roles disponíveis:** `customer`, `agent`, `admin`

**Response:**
```json
{
  "id": 1,
  "email": "usuario@email.com",
  "full_name": "Nome do Usuário",
  "role": "customer",
  "is_active": true,
  "is_online": false,
  "created_at": "2024-01-01T00:00:00"
}
```

### Login
**POST** `/auth/login`

**Body (form-data):**
```
username: usuario@email.com
password: senha123456
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Logout
**POST** `/auth/logout`

**Headers:** Authorization Bearer Token

**Response:**
```json
{
  "message": "Logout realizado com sucesso"
}
```

---

## 🎫 Tickets

### Listar Tickets
**GET** `/tickets/`

**Query Parameters:**
- `status_filter` (opcional): open, in_progress, waiting, resolved, closed
- `priority` (opcional): low, medium, high, urgent
- `skip` (opcional): número de registros a pular (padrão: 0)
- `limit` (opcional): número de registros a retornar (padrão: 50)

**Response:**
```json
[
  {
    "id": 1,
    "title": "Problema com login",
    "description": "Não consigo fazer login no sistema",
    "status": "open",
    "priority": "high",
    "category": "Técnico",
    "customer_id": 1,
    "assigned_to": null,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
]
```

### Criar Ticket
**POST** `/tickets/`

**Body:**
```json
{
  "title": "Problema com login",
  "description": "Não consigo fazer login no sistema",
  "priority": "high",
  "category": "Técnico"
}
```

### Obter Ticket
**GET** `/tickets/{ticket_id}`

### Atualizar Ticket
**PATCH** `/tickets/{ticket_id}`

**Body:**
```json
{
  "status": "in_progress",
  "assigned_to": 2
}
```

### Deletar Ticket
**DELETE** `/tickets/{ticket_id}`

*Apenas admin*

### Listar Mensagens do Ticket
**GET** `/tickets/{ticket_id}/messages`

### Criar Mensagem no Ticket
**POST** `/tickets/{ticket_id}/messages`

**Body:**
```json
{
  "content": "Obrigado por reportar. Estamos investigando.",
  "is_internal": false
}
```

---

## 💬 Chat ao Vivo

### Criar Sessão de Chat
**POST** `/chats/`

**Response:**
```json
{
  "id": 1,
  "status": "waiting",
  "customer_id": 1,
  "agent_id": null,
  "started_at": "2024-01-01T00:00:00"
}
```

### Listar Sessões de Chat
**GET** `/chats/`

**Query Parameters:**
- `status_filter` (opcional): active, waiting, ended
- `skip` (opcional)
- `limit` (opcional)

### Obter Chats Aguardando
**GET** `/chats/waiting`

*Apenas agentes e admins*

### Aceitar Chat
**POST** `/chats/{session_id}/accept`

*Apenas agentes e admins*

### Enviar Mensagem no Chat
**POST** `/chats/{session_id}/messages`

**Body:**
```json
{
  "content": "Olá! Como posso ajudar?"
}
```

### Listar Mensagens do Chat
**GET** `/chats/{session_id}/messages`

### Atualizar Sessão de Chat
**PATCH** `/chats/{session_id}`

**Body:**
```json
{
  "status": "ended",
  "rating": 5,
  "feedback": "Ótimo atendimento!"
}
```

---

## 📚 Base de Conhecimento

### Listar Artigos
**GET** `/knowledge/`

**Query Parameters:**
- `search` (opcional): busca em título, conteúdo e tags
- `category` (opcional): filtrar por categoria
- `published_only` (opcional): apenas publicados (padrão: true)
- `skip` (opcional)
- `limit` (opcional)

**Response:**
```json
[
  {
    "id": 1,
    "title": "Como resetar minha senha",
    "content": "Para resetar sua senha...",
    "category": "Conta",
    "tags": "senha,login,recuperação",
    "author_id": 2,
    "is_published": true,
    "view_count": 150,
    "helpful_count": 45,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00",
    "published_at": "2024-01-01T00:00:00"
  }
]
```

### Criar Artigo
**POST** `/knowledge/`

*Apenas agentes e admins*

**Body:**
```json
{
  "title": "Como resetar minha senha",
  "content": "Para resetar sua senha, siga estes passos...",
  "category": "Conta",
  "tags": "senha,login,recuperação"
}
```

### Obter Artigo
**GET** `/knowledge/{article_id}`

*Incrementa contador de visualizações*

### Atualizar Artigo
**PATCH** `/knowledge/{article_id}`

*Apenas agentes e admins*

**Body:**
```json
{
  "is_published": true
}
```

### Deletar Artigo
**DELETE** `/knowledge/{article_id}`

*Apenas admins*

### Marcar Artigo como Útil
**POST** `/knowledge/{article_id}/helpful`

*Incrementa contador de utilidade*

### Listar Categorias
**GET** `/knowledge/categories/list`

**Response:**
```json
["Conta", "Técnico", "Pagamento", "Geral"]
```

---

## 🔑 Códigos de Status HTTP

- `200 OK` - Requisição bem-sucedida
- `201 Created` - Recurso criado com sucesso
- `204 No Content` - Recurso deletado com sucesso
- `400 Bad Request` - Requisição inválida
- `401 Unauthorized` - Não autenticado
- `403 Forbidden` - Sem permissão
- `404 Not Found` - Recurso não encontrado
- `422 Unprocessable Entity` - Erro de validação
- `500 Internal Server Error` - Erro no servidor

---

## 📊 Exemplos de Uso

### Exemplo 1: Criar Conta e Fazer Login

```bash
# 1. Registrar
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "teste@email.com",
    "full_name": "Usuário Teste",
    "password": "senha123456",
    "role": "customer"
  }'

# 2. Fazer Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -F "username=teste@email.com" \
  -F "password=senha123456"

# Salve o access_token retornado
```

### Exemplo 2: Criar e Listar Tickets

```bash
# Definir token
TOKEN="seu_token_aqui"

# Criar ticket
curl -X POST http://localhost:8000/api/v1/tickets/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Problema ao fazer upload",
    "description": "Não consigo fazer upload de arquivos grandes",
    "priority": "medium",
    "category": "Técnico"
  }'

# Listar tickets
curl -X GET http://localhost:8000/api/v1/tickets/ \
  -H "Authorization: Bearer $TOKEN"
```

### Exemplo 3: Buscar na Base de Conhecimento

```bash
# Buscar artigos sobre senha
curl -X GET "http://localhost:8000/api/v1/knowledge/?search=senha&published_only=true"

# Obter artigo específico
curl -X GET http://localhost:8000/api/v1/knowledge/1
```

---

## 🧪 Testando com Swagger UI

Acesse http://localhost:8000/api/docs para testar todos os endpoints interativamente.

1. Clique em **Authorize** no topo
2. Faça login e copie o `access_token`
3. Cole no formato: `Bearer seu_token_aqui`
4. Agora você pode testar todos os endpoints protegidos

---

## 📝 Notas Importantes

- Tokens JWT expiram em 24 horas (configurável)
- Senhas devem ter no mínimo 8 caracteres
- Mensagens internas (is_internal=true) só são visíveis para agentes/admins
- Clientes só veem seus próprios tickets e chats
- Artigos não publicados só são visíveis para agentes/admins

---

Para mais informações, consulte a documentação completa em:
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

