# Diagrama ER (Entity-Relationship) - Banco de Dados

## Sistema de Suporte ao Cliente - Database Schema

### Descrição
Este diagrama mostra todas as entidades do banco de dados PostgreSQL, seus campos, tipos de dados e relacionamentos.

---

## Diagrama ER

```
┌─────────────────────────────────────────┐
│              USERS                       │
├─────────────────────────────────────────┤
│ PK │ id                 INTEGER          │
│    │ email              VARCHAR UNIQUE   │
│    │ full_name          VARCHAR          │
│    │ hashed_password    VARCHAR          │
│    │ role               ENUM             │
│    │ is_active          BOOLEAN          │
│    │ is_online          BOOLEAN          │
│    │ avatar_url         VARCHAR NULL     │
│    │ created_at         TIMESTAMP        │
│    │ updated_at         TIMESTAMP        │
└──────────┬──────────────────────────────┘
           │
           │ 1:N (customer)
           │
     ┌─────▼────────────────────────────────────┐
     │              TICKETS                      │
     ├───────────────────────────────────────────┤
     │ PK │ id                 INTEGER           │
     │    │ title              VARCHAR           │
     │    │ description        TEXT              │
     │    │ status             ENUM              │
     │    │ priority           ENUM              │
     │    │ category           VARCHAR NULL      │
     │ FK │ customer_id        INTEGER           │─┐
     │ FK │ assigned_to        INTEGER NULL      │ │
     │    │ created_at         TIMESTAMP         │ │
     │    │ updated_at         TIMESTAMP         │ │
     │    │ resolved_at        TIMESTAMP NULL    │ │
     │    │ closed_at          TIMESTAMP NULL    │ │
     └──────────┬───────────────────────────────┬─┘ │
                │                               │   │
                │ 1:N                           │   │
                │                               │   │ 1:N (agent)
     ┌──────────▼──────────────────┐            │   │
     │       MESSAGES               │            │   │
     ├──────────────────────────────┤            │   │
     │ PK │ id           INTEGER    │            │   │
     │    │ content      TEXT       │            │   │
     │    │ is_internal  BOOLEAN    │            │   │
     │ FK │ ticket_id    INT NULL   │────────────┘   │
     │ FK │ chat_session_id INT NULL│                │
     │ FK │ sender_id    INTEGER    │────────────────┼─┐
     │    │ created_at   TIMESTAMP  │                │ │
     │    │ read_at      TIMESTAMP  │                │ │
     └─────────────────────────────┘                │ │
                                                    │ │
           ┌────────────────────────────────────────┘ │
           │                                          │
           │ 1:N (customer)                           │
           │                                          │
     ┌─────▼────────────────────────────────┐        │
     │        CHAT_SESSIONS                  │        │
     ├───────────────────────────────────────┤        │
     │ PK │ id           INTEGER             │        │
     │    │ status       ENUM                │        │
     │ FK │ customer_id  INTEGER             │────────┘
     │ FK │ agent_id     INTEGER NULL        │────────┐
     │    │ started_at   TIMESTAMP           │        │
     │    │ ended_at     TIMESTAMP NULL      │        │
     │    │ rating       INTEGER NULL        │        │
     │    │ feedback     TEXT NULL           │        │
     └──────────────────────────────────────┘        │
                                                      │ 1:N (agent)
           ┌──────────────────────────────────────────┘
           │
           │ 1:N (author)
           │
     ┌─────▼────────────────────────────────┐
     │     KNOWLEDGE_ARTICLES                │
     ├───────────────────────────────────────┤
     │ PK │ id             INTEGER           │
     │    │ title          VARCHAR           │
     │    │ content        TEXT              │
     │    │ category       VARCHAR NULL      │
     │    │ tags           VARCHAR NULL      │
     │ FK │ author_id      INTEGER           │
     │    │ is_published   BOOLEAN           │
     │    │ view_count     INTEGER           │
     │    │ helpful_count  INTEGER           │
     │    │ created_at     TIMESTAMP         │
     │    │ updated_at     TIMESTAMP         │
     │    │ published_at   TIMESTAMP NULL    │
     └──────────────────────────────────────┘
```

---

## Entidades

### 1. USERS
**Descrição**: Usuários do sistema (clientes, agentes, admins)

| Coluna | Tipo | Constraints | Descrição |
|--------|------|-------------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT | Identificador único |
| email | VARCHAR(255) | UNIQUE, NOT NULL, INDEX | Email do usuário |
| full_name | VARCHAR(255) | NOT NULL | Nome completo |
| hashed_password | VARCHAR(255) | NOT NULL | Senha hasheada (bcrypt) |
| role | ENUM | NOT NULL, DEFAULT 'customer' | customer, agent, admin |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | Usuário ativo |
| is_online | BOOLEAN | NOT NULL, DEFAULT FALSE | Status online |
| avatar_url | VARCHAR(500) | NULL | URL do avatar |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Data de criação |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Última atualização |

**Relacionamentos:**
- 1:N → tickets (como customer)
- 1:N → tickets (como agent assigned)
- 1:N → messages (como sender)
- 1:N → chat_sessions (como customer)
- 1:N → chat_sessions (como agent)
- 1:N → knowledge_articles (como author)

---

### 2. TICKETS
**Descrição**: Tickets de suporte

| Coluna | Tipo | Constraints | Descrição |
|--------|------|-------------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT | Identificador único |
| title | VARCHAR(200) | NOT NULL, INDEX | Título do ticket |
| description | TEXT | NOT NULL | Descrição detalhada |
| status | ENUM | NOT NULL, DEFAULT 'open', INDEX | open, in_progress, waiting, resolved, closed |
| priority | ENUM | NOT NULL, DEFAULT 'medium' | low, medium, high, urgent |
| category | VARCHAR(100) | NULL, INDEX | Categoria do problema |
| customer_id | INTEGER | FK users(id), NOT NULL, INDEX | Cliente que criou |
| assigned_to | INTEGER | FK users(id), NULL, INDEX | Agente atribuído |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW(), INDEX | Data de criação |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Última atualização |
| resolved_at | TIMESTAMP | NULL | Data de resolução |
| closed_at | TIMESTAMP | NULL | Data de fechamento |

**Relacionamentos:**
- N:1 → users (customer)
- N:1 → users (assigned agent)
- 1:N → messages

---

### 3. MESSAGES
**Descrição**: Mensagens de tickets e chats

| Coluna | Tipo | Constraints | Descrição |
|--------|------|-------------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT | Identificador único |
| content | TEXT | NOT NULL | Conteúdo da mensagem |
| is_internal | BOOLEAN | NOT NULL, DEFAULT FALSE | Nota interna (apenas agentes) |
| ticket_id | INTEGER | FK tickets(id), NULL, INDEX | Ticket relacionado |
| chat_session_id | INTEGER | FK chat_sessions(id), NULL, INDEX | Chat relacionado |
| sender_id | INTEGER | FK users(id), NOT NULL, INDEX | Quem enviou |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW(), INDEX | Data de envio |
| read_at | TIMESTAMP | NULL | Data de leitura |

**Constraints:**
- CHECK: (ticket_id IS NOT NULL) OR (chat_session_id IS NOT NULL)
- Uma mensagem pertence a um ticket OU a um chat

**Relacionamentos:**
- N:1 → tickets (opcional)
- N:1 → chat_sessions (opcional)
- N:1 → users (sender)

---

### 4. CHAT_SESSIONS
**Descrição**: Sessões de chat ao vivo

| Coluna | Tipo | Constraints | Descrição |
|--------|------|-------------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT | Identificador único |
| status | ENUM | NOT NULL, DEFAULT 'waiting', INDEX | waiting, active, ended |
| customer_id | INTEGER | FK users(id), NOT NULL, INDEX | Cliente |
| agent_id | INTEGER | FK users(id), NULL, INDEX | Agente atribuído |
| started_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Início do chat |
| ended_at | TIMESTAMP | NULL | Fim do chat |
| rating | INTEGER | NULL, CHECK (1-5) | Avaliação (1-5 estrelas) |
| feedback | TEXT | NULL | Feedback do cliente |

**Relacionamentos:**
- N:1 → users (customer)
- N:1 → users (agent)
- 1:N → messages

---

### 5. KNOWLEDGE_ARTICLES
**Descrição**: Artigos da base de conhecimento

| Coluna | Tipo | Constraints | Descrição |
|--------|------|-------------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT | Identificador único |
| title | VARCHAR(200) | NOT NULL, INDEX | Título do artigo |
| content | TEXT | NOT NULL | Conteúdo completo |
| category | VARCHAR(100) | NULL, INDEX | Categoria |
| tags | VARCHAR(500) | NULL | Tags separadas por vírgula |
| author_id | INTEGER | FK users(id), NOT NULL | Autor do artigo |
| is_published | BOOLEAN | NOT NULL, DEFAULT FALSE | Publicado |
| view_count | INTEGER | NOT NULL, DEFAULT 0 | Contador de visualizações |
| helpful_count | INTEGER | NOT NULL, DEFAULT 0 | Contador de "útil" |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Data de criação |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Última atualização |
| published_at | TIMESTAMP | NULL | Data de publicação |

**Relacionamentos:**
- N:1 → users (author)

---

## Enums

### UserRole
```sql
CREATE TYPE user_role AS ENUM ('admin', 'agent', 'customer');
```

### TicketStatus
```sql
CREATE TYPE ticket_status AS ENUM (
    'open',
    'in_progress',
    'waiting',
    'resolved',
    'closed'
);
```

### TicketPriority
```sql
CREATE TYPE ticket_priority AS ENUM ('low', 'medium', 'high', 'urgent');
```

### ChatStatus
```sql
CREATE TYPE chat_status AS ENUM ('active', 'waiting', 'ended');
```

---

## Constraints e Regras

### Foreign Keys
- ON DELETE CASCADE: messages (quando ticket/chat deletado)
- ON DELETE SET NULL: tickets.assigned_to, chat_sessions.agent_id
- ON DELETE RESTRICT: customer_id, author_id (não pode deletar usuário com dados)

### Checks
- messages: Deve ter ticket_id OU chat_session_id
- chat_sessions.rating: Entre 1 e 5
- users.role: Deve ser um dos valores do enum

### Unique Constraints
- users.email: Único (não pode duplicar emails)

---

## Volumes de Dados Estimados

| Tabela | Registros (1 ano) | Crescimento |
|--------|-------------------|-------------|
| users | 10.000 | 1.000/mês |
| tickets | 100.000 | 10.000/mês |
| messages | 500.000 | 50.000/mês |
| chat_sessions | 50.000 | 5.000/mês |
| knowledge_articles | 1.000 | 100/mês |

---

## Estratégia de Backup

1. **Backup completo**: Diário (3am)
2. **WAL archiving**: Contínuo
3. **Retenção**: 30 dias
4. **Point-in-time recovery**: Habilitado

---

## Decisões Arquiteturais Relacionadas
- [ADR 002: PostgreSQL Database](../adr/002-uso-postgresql-database.md)
- [ADR 006: Estrutura Modular Backend](../adr/006-estrutura-modular-backend.md)

---

**Versão**: 1.0
**Data**: 2024-12-07
**Autores**: Database Engineer, Backend Developer

