# Índices do Banco de Dados - Estratégia de Performance

## Índices Implementados no PostgreSQL

### Descrição
Este documento detalha todos os índices criados no banco de dados para otimizar performance de queries.

---

## Índices por Tabela

### 1. USERS

| Índice | Tipo | Colunas | Justificativa |
|--------|------|---------|---------------|
| users_pkey | B-tree | id | Primary key (auto) |
| users_email_key | B-tree | email | UNIQUE constraint, login queries |
| idx_users_role | B-tree | role | Filtrar por tipo de usuário |
| idx_users_is_active | B-tree | is_active | Filtrar usuários ativos |

**Queries otimizadas:**
```sql
-- Login (muito frequente)
SELECT * FROM users WHERE email = 'user@email.com';

-- Listar agentes ativos
SELECT * FROM users WHERE role = 'agent' AND is_active = TRUE;
```

**Performance esperada:**
- Login: < 1ms (index scan)
- Filtro por role: < 5ms

---

### 2. TICKETS

| Índice | Tipo | Colunas | Justificativa |
|--------|------|---------|---------------|
| tickets_pkey | B-tree | id | Primary key (auto) |
| idx_tickets_customer_id | B-tree | customer_id | FK, listar tickets do cliente |
| idx_tickets_assigned_to | B-tree | assigned_to | FK, listar tickets do agente |
| idx_tickets_status | B-tree | status | Filtrar por status (muito comum) |
| idx_tickets_created_at | BRIN | created_at | Range queries em timestamps |
| idx_tickets_composite | B-tree | (customer_id, status) | Query mais comum: tickets do cliente por status |

**Queries otimizadas:**
```sql
-- Tickets do cliente (dashboard principal)
SELECT * FROM tickets 
WHERE customer_id = 123 
ORDER BY created_at DESC;

-- Tickets abertos do agente
SELECT * FROM tickets 
WHERE assigned_to = 456 AND status = 'open';

-- Tickets por período
SELECT * FROM tickets 
WHERE created_at >= '2024-01-01' 
AND created_at < '2024-02-01';
```

**Performance esperada:**
- Listar tickets do cliente: < 10ms
- Filtrar por status: < 20ms
- Range queries: < 50ms (BRIN)

---

### 3. MESSAGES

| Índice | Tipo | Colunas | Justificativa |
|--------|------|---------|---------------|
| messages_pkey | B-tree | id | Primary key (auto) |
| idx_messages_ticket_id | B-tree | ticket_id | FK, listar mensagens do ticket |
| idx_messages_chat_session_id | B-tree | chat_session_id | FK, listar mensagens do chat |
| idx_messages_sender_id | B-tree | sender_id | FK, histórico do usuário |
| idx_messages_created_at | BRIN | created_at | Ordenação temporal |

**Queries otimizadas:**
```sql
-- Mensagens do ticket (muito frequente)
SELECT * FROM messages 
WHERE ticket_id = 789 
ORDER BY created_at ASC;

-- Mensagens do chat
SELECT * FROM messages 
WHERE chat_session_id = 456 
ORDER BY created_at ASC;
```

**Performance esperada:**
- Carregar mensagens: < 5ms
- Ordenação temporal: < 10ms

---

### 4. CHAT_SESSIONS

| Índice | Tipo | Colunas | Justificativa |
|--------|------|---------|---------------|
| chat_sessions_pkey | B-tree | id | Primary key (auto) |
| idx_chat_customer_id | B-tree | customer_id | FK, chats do cliente |
| idx_chat_agent_id | B-tree | agent_id | FK, chats do agente |
| idx_chat_status | B-tree | status | Filtrar por status (fila de espera) |
| idx_chat_started_at | BRIN | started_at | Ordenação temporal |

**Queries otimizadas:**
```sql
-- Chats aguardando atendimento (crítico)
SELECT * FROM chat_sessions 
WHERE status = 'waiting' 
ORDER BY started_at ASC;

-- Histórico de chats do cliente
SELECT * FROM chat_sessions 
WHERE customer_id = 123 
ORDER BY started_at DESC;
```

**Performance esperada:**
- Fila de espera: < 5ms (crítico para UX)
- Histórico: < 10ms

---

### 5. KNOWLEDGE_ARTICLES

| Índice | Tipo | Colunas | Justificativa |
|--------|------|---------|---------------|
| knowledge_articles_pkey | B-tree | id | Primary key (auto) |
| idx_articles_author_id | B-tree | author_id | FK, artigos do autor |
| idx_articles_category | B-tree | category | Filtrar por categoria |
| idx_articles_is_published | B-tree | is_published | Apenas artigos publicados |
| idx_articles_title | GIN | to_tsvector('portuguese', title) | Full-text search em título |
| idx_articles_content | GIN | to_tsvector('portuguese', content) | Full-text search em conteúdo |
| idx_articles_view_count | B-tree | view_count DESC | Ordenar por popularidade |

**Queries otimizadas:**
```sql
-- Busca full-text (feature principal)
SELECT * FROM knowledge_articles 
WHERE is_published = TRUE 
AND (
    to_tsvector('portuguese', title) @@ to_tsquery('portuguese', 'senha')
    OR to_tsvector('portuguese', content) @@ to_tsquery('portuguese', 'senha')
);

-- Artigos mais visualizados
SELECT * FROM knowledge_articles 
WHERE is_published = TRUE 
ORDER BY view_count DESC 
LIMIT 10;

-- Artigos por categoria
SELECT * FROM knowledge_articles 
WHERE is_published = TRUE 
AND category = 'Conta';
```

**Performance esperada:**
- Full-text search: < 50ms (GIN index)
- Top artigos: < 10ms
- Por categoria: < 15ms

---

## Tipos de Índices Utilizados

### B-tree (Maioria dos casos)
**Uso**: Igualdade, range queries, ORDER BY
**Vantagens**: 
- Versátil, funciona para a maioria dos casos
- Eficiente para igualdade e comparações
- Suporta ordenação

**Exemplos:**
- Primary keys
- Foreign keys
- Filtros comuns (status, role)

---

### GIN (Generalized Inverted Index)
**Uso**: Full-text search, arrays
**Vantagens**:
- Excelente para text search
- Busca em arrays
- Operadores especiais (@@ para tsquery)

**Exemplos:**
- Busca em artigos (título e conteúdo)
- Tags (futuro)

---

### BRIN (Block Range Index)
**Uso**: Timestamps, dados sequenciais
**Vantagens**:
- Muito pequeno (< 1% do B-tree)
- Eficiente para range queries
- Ótimo para dados append-only

**Exemplos:**
- created_at
- updated_at
- started_at

**Limitações:**
- Requer dados fisicamente ordenados
- Menos preciso que B-tree

---

## Índices Compostos

### tickets (customer_id, status)
```sql
CREATE INDEX idx_tickets_composite 
ON tickets (customer_id, status);
```

**Justificativa**: Query mais comum no dashboard
```sql
SELECT * FROM tickets 
WHERE customer_id = ? AND status = 'open';
```

**Performance**: Index-only scan, < 5ms

---

## Estratégia de Manutenção

### VACUUM e ANALYZE
```sql
-- Automático (autovacuum enabled)
-- Manual quando necessário:
VACUUM ANALYZE tickets;
VACUUM ANALYZE messages;
```

### REINDEX
```sql
-- Apenas se índice corrompido ou muito fragmentado
REINDEX TABLE tickets;
```

### Monitoring
```sql
-- Ver uso de índices
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;

-- Índices não utilizados (candidatos à remoção)
SELECT 
    schemaname,
    tablename,
    indexname
FROM pg_stat_user_indexes
WHERE idx_scan = 0 
AND indexrelname NOT LIKE '%_pkey';
```

---

## Trade-offs

### Vantagens dos Índices:
- ✅ Queries rápidas (10-100x mais rápido)
- ✅ Melhor experiência do usuário
- ✅ Reduz carga no CPU

### Desvantagens dos Índices:
- ⚠️ Espaço em disco (estimado: +30% do tamanho das tabelas)
- ⚠️ INSERT/UPDATE mais lentos (5-10% overhead)
- ⚠️ Manutenção (vacuum, analyze)

### Decisão:
**Priorizamos read performance** porque:
- Sistema é read-heavy (90% reads, 10% writes)
- UX depende de queries rápidas
- Espaço em disco é barato
- Write overhead é aceitável

---

## Performance Targets

| Operação | Target | Com índices | Sem índices |
|----------|--------|-------------|-------------|
| Login | < 100ms | 1ms ✅ | 500ms ❌ |
| Listar tickets | < 200ms | 10ms ✅ | 2000ms ❌ |
| Carregar mensagens | < 100ms | 5ms ✅ | 500ms ❌ |
| Busca em artigos | < 500ms | 50ms ✅ | 5000ms ❌ |
| Fila de chat | < 100ms | 5ms ✅ | 1000ms ❌ |

---

## Índices Futuros (Planejados)

### Quando adicionar:
- [ ] Índice parcial para tickets abertos
```sql
CREATE INDEX idx_tickets_open 
ON tickets (customer_id) 
WHERE status IN ('open', 'in_progress');
```

- [ ] Índice trigram para busca fuzzy
```sql
CREATE EXTENSION pg_trgm;
CREATE INDEX idx_articles_title_trgm 
ON knowledge_articles 
USING gin (title gin_trgm_ops);
```

- [ ] Índice para tags (quando implementado)
```sql
CREATE INDEX idx_articles_tags 
ON knowledge_articles 
USING gin (string_to_array(tags, ','));
```

---

## Decisões Arquiteturais Relacionadas
- [ADR 002: PostgreSQL Database](../adr/002-uso-postgresql-database.md)

---

**Versão**: 1.0
**Data**: 2024-12-07
**Autores**: Database Engineer, Backend Developer

