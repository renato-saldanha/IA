# C4 Model - Level 2: Container Diagram

## Sistema de Suporte ao Cliente - Containers

### Descrição
Este diagrama mostra os containers (aplicações, data stores) que compõem o sistema de suporte ao cliente e como eles se comunicam.

---

## Diagrama

```
                         ┌──────────────────────────────────────┐
                         │         USUÁRIOS                     │
                         │  Cliente | Agente | Admin            │
                         └──────────────┬───────────────────────┘
                                        │
                                        │ HTTPS
                                        │
                         ┌──────────────▼───────────────────────┐
                         │                                      │
                         │   FRONTEND WEB APPLICATION           │
                         │   [Next.js 15 + React 18]            │
                         │   - Server/Client Components         │
                         │   - TypeScript                       │
                         │   - Tailwind CSS                     │
                         │   - Responsive UI                    │
                         │                                      │
                         │   Port: 3000                         │
                         └──────────────┬───────────────────────┘
                                        │
                                        │ HTTP/REST
                                        │ JSON
                                        │
                         ┌──────────────▼───────────────────────┐
                         │                                      │
                         │   BACKEND API APPLICATION            │
                         │   [FastAPI + Python 3.11]            │
                         │   - RESTful API                      │
                         │   - JWT Authentication               │
                         │   - OpenAPI/Swagger                  │
                         │   - Async operations                 │
                         │                                      │
                         │   Port: 8000                         │
                         └─────┬──────────────────┬─────────────┘
                               │                  │
                    ┌──────────▼──────┐     ┌────▼──────────┐
                    │                 │     │               │
                    │   PostgreSQL    │     │    Redis      │
                    │   [Database]    │     │   [Cache]     │
                    │                 │     │               │
                    │   - User data   │     │   - Sessions  │
                    │   - Tickets     │     │   - Chat      │
                    │   - Messages    │     │   - Rate      │
                    │   - Articles    │     │     limiting  │
                    │                 │     │               │
                    │   Port: 5432    │     │   Port: 6379  │
                    └─────────────────┘     └───────────────┘
```

---

## Containers

### 1. Frontend Web Application
**Tecnologia**: Next.js 15 + React 18 + TypeScript
**Responsabilidade**: Interface do usuário e experiência

**Detalhes:**
- **Framework**: Next.js 15 (App Router)
- **UI Library**: React 18 (Server + Client Components)
- **Language**: TypeScript 5.3
- **Styling**: Tailwind CSS 3.4
- **Icons**: Lucide React
- **HTTP Client**: Axios
- **State**: React Query (planejado)
- **Forms**: React Hook Form + Zod

**Features:**
- Páginas de autenticação (login/registro)
- Dashboard de tickets
- Interface de chat ao vivo
- Portal de base de conhecimento
- Responsivo (mobile, tablet, desktop)

**Deployment**: Vercel (recomendado)
**Port**: 3000

**Comunicação:**
- ← Usuários via HTTPS (navegador)
- → Backend API via HTTP/REST (JSON)

---

### 2. Backend API Application
**Tecnologia**: FastAPI + Python 3.11
**Responsabilidade**: Lógica de negócio e APIs

**Detalhes:**
- **Framework**: FastAPI 0.109
- **Language**: Python 3.11
- **ORM**: SQLAlchemy 2.0 (async)
- **Validation**: Pydantic v2
- **Auth**: JWT (python-jose)
- **Password**: Bcrypt (passlib)
- **Server**: Uvicorn (ASGI)
- **Migrations**: Alembic

**APIs (25+ endpoints):**
- `/api/v1/auth/*` - Autenticação
- `/api/v1/tickets/*` - Sistema de tickets
- `/api/v1/chats/*` - Chat ao vivo
- `/api/v1/knowledge/*` - Base de conhecimento

**Features:**
- Autenticação JWT stateless
- RBAC (Role-Based Access Control)
- Validação de inputs
- Rate limiting
- Docs automática (Swagger UI)
- CORS configurado

**Deployment**: Railway / Render / AWS
**Port**: 8000

**Comunicação:**
- ← Frontend via HTTP/REST (JSON)
- → PostgreSQL via SQLAlchemy (SQL)
- → Redis via redis-py (Protocol)

---

### 3. PostgreSQL Database
**Tecnologia**: PostgreSQL 16
**Responsabilidade**: Armazenamento persistente

**Detalhes:**
- **Version**: PostgreSQL 16 (Alpine)
- **Driver**: psycopg2-binary
- **Connection**: SQLAlchemy pool

**Schemas principais:**
- `users` - Usuários (cliente, agente, admin)
- `tickets` - Tickets de suporte
- `messages` - Mensagens (tickets + chat)
- `chat_sessions` - Sessões de chat
- `knowledge_articles` - Artigos da base

**Índices:**
- B-tree: chaves estrangeiras, email
- GIN: full-text search em artigos
- BRIN: timestamps (created_at, updated_at)

**Features:**
- ACID transactions
- Full-text search nativo
- Relacionamentos complexos
- Triggers e constraints

**Deployment**: Managed service (Railway/AWS RDS)
**Port**: 5432

**Comunicação:**
- ← Backend API via SQLAlchemy (SQL queries)

---

### 4. Redis Cache
**Tecnologia**: Redis 7
**Responsabilidade**: Cache e dados temporários

**Detalhes:**
- **Version**: Redis 7 (Alpine)
- **Driver**: redis-py
- **Persistence**: AOF enabled

**Uso:**
- **Cache**: Artigos frequentes, categorias
- **Sessions**: Estado de chat ativo
- **Rate limiting**: Tentativas de login
- **Presence**: Agentes online
- **Counters**: View counts (batch write)

**Data structures:**
- Strings: cache de queries
- Sets: agentes online
- Hashes: session data
- Sorted Sets: rankings (futuro)

**TTL Strategy:**
- Cache: 1 hora
- Sessions: 24 horas
- Rate limits: 5 minutos

**Deployment**: Managed service (Railway/Upstash)
**Port**: 6379

**Comunicação:**
- ← Backend API via redis-py (Redis protocol)

---

## Fluxo de Dados

### Exemplo 1: Cliente cria ticket

```
1. Cliente preenche formulário → Frontend valida
2. Frontend POST /api/v1/tickets/ → Backend
3. Backend valida com Pydantic → cria registro
4. Backend INSERT INTO tickets → PostgreSQL
5. Backend retorna TicketResponse → Frontend
6. Frontend atualiza UI → Cliente vê confirmação
```

### Exemplo 2: Busca em artigos (com cache)

```
1. Cliente busca "senha" → Frontend
2. Frontend GET /api/v1/knowledge/?search=senha → Backend
3. Backend verifica cache → Redis (cache hit)
4. Redis retorna artigos → Backend
5. Backend retorna JSON → Frontend
6. Frontend renderiza resultados
```

### Exemplo 3: Chat ao vivo

```
1. Cliente inicia chat → Frontend
2. Frontend POST /api/v1/chats/ → Backend
3. Backend cria session → PostgreSQL + Redis
4. Agente aceita → Backend atualiza status
5. Mensagens trafegam → Backend (futuro: WebSockets)
6. Chat finalizado → Métricas no PostgreSQL
```

---

## Comunicação entre Containers

### Protocols:
- **Frontend ↔ Backend**: HTTP/REST (JSON)
- **Backend ↔ PostgreSQL**: TCP/SQL (via SQLAlchemy)
- **Backend ↔ Redis**: TCP/Redis Protocol (via redis-py)

### Authentication:
- Frontend armazena JWT token (localStorage)
- Cada request: `Authorization: Bearer <token>`
- Backend valida token antes de processar

### Network (Docker Compose):
- Todos containers na mesma rede Docker
- Comunicação por nome do serviço
- Frontend → `http://backend:8000`
- Backend → `postgres:5432`, `redis:6379`

---

## Segurança

### Frontend:
- HTTPS obrigatório em produção
- XSS prevention (React escape)
- CSRF protection (SameSite cookies)
- Input sanitization

### Backend:
- JWT validation em todos endpoints
- Rate limiting (10 req/s por IP)
- Input validation (Pydantic)
- SQL injection prevention (ORM)
- CORS configurado

### Database:
- Credenciais em variáveis de ambiente
- Conexões SSL em produção
- User com privilégios limitados
- Backups automáticos

### Redis:
- Sem autenticação (rede interna)
- Em produção: AUTH password
- TTL em todos keys

---

## Escalabilidade

### Horizontal Scaling:

**Frontend:**
- Stateless (pode ter N instâncias)
- Deploy: Vercel Edge Network

**Backend:**
- Stateless (JWT, sem sessões)
- Load balancer + N workers
- Deploy: Railway autoscaling

**PostgreSQL:**
- Read replicas para queries
- Connection pooling (SQLAlchemy)
- PgBouncer se necessário

**Redis:**
- Clustering para alta disponibilidade
- Sentinel para failover

---

## Monitoramento

### Logs:
- Frontend: Vercel logs / LogRocket
- Backend: Railway logs / Datadog
- Database: PostgreSQL slow query log
- Redis: redis-cli MONITOR (dev only)

### Metrics:
- Request rate, latency
- Error rates (4xx, 5xx)
- Database connections
- Cache hit ratio

### Health Checks:
- Frontend: Vercel automatic
- Backend: `/health` endpoint
- PostgreSQL: `pg_isready`
- Redis: `redis-cli ping`

---

## Decisões Arquiteturais Relacionadas
- [ADR 001: FastAPI Backend](../adr/001-escolha-fastapi-backend.md)
- [ADR 002: PostgreSQL Database](../adr/002-uso-postgresql-database.md)
- [ADR 004: Docker Compose](../adr/004-containerizacao-docker.md)
- [ADR 005: Next.js Frontend](../adr/005-frontend-nextjs-typescript.md)
- [ADR 007: Redis Cache](../adr/007-redis-cache-chat.md)

---

**Versão**: 1.0
**Data**: 2024-12-07
**Autores**: Tech Lead, Software Architect, DevOps Engineer

