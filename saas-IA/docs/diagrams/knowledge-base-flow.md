# Fluxo da Base de Conhecimento

## Descrição
Fluxo completo da base de conhecimento: criação, publicação, busca e métricas.

---

## 1. Fluxo de Criação de Artigo (Agente)

```
Agente → Frontend → Backend → PostgreSQL

1. Agente acessa /dashboard/knowledge
2. Clica "Novo Artigo"
3. Preenche formulário:
   - Título
   - Conteúdo (Markdown/Rich text)
   - Categoria
   - Tags
4. Salva como rascunho (is_published=FALSE)
5. Backend INSERT INTO knowledge_articles
6. Artigo visível apenas para agentes/admins
```

---

## 2. Fluxo de Publicação

```
Agente/Admin → Frontend → Backend → PostgreSQL

1. Agente revisa artigo
2. Clica "Publicar"
3. Backend UPDATE:
   - is_published = TRUE
   - published_at = NOW()
4. Artigo agora visível para todos
```

---

## 3. Fluxo de Busca (Cliente)

```
Cliente          Frontend         Backend          PostgreSQL       Redis
  │                │                │                  │              │
  │ 1. Acessa      │                │                  │              │
  │   /knowledge   │                │                  │              │
  │───────────────>│ 2. GET         │                  │              │
  │                │  /knowledge/   │                  │              │
  │                │───────────────>│                  │              │
  │                │                │ 3. Check cache   │              │
  │                │                │─────────────────────────────────>│
  │                │                │                  │ Cache miss   │
  │                │                │ 4. SELECT        │              │
  │                │                │  articles        │              │
  │                │                │  WHERE           │              │
  │                │                │  is_published    │              │
  │                │                │─────────────────>│              │
  │                │                │                  │ 5. Cache     │
  │                │                │  SET articles    │              │
  │                │                │─────────────────────────────────>│
  │                │<───────────────│ Lista artigos    │              │
  │<───────────────│                │                  │              │
  │                │                │                  │              │
  │ 6. Busca       │                │                  │              │
  │  "resetar      │                │                  │              │
  │   senha"       │                │                  │              │
  │───────────────>│ 7. GET         │                  │              │
  │                │  ?search=...   │                  │              │
  │                │───────────────>│                  │              │
  │                │                │ 8. Full-text     │              │
  │                │                │  search (GIN)    │              │
  │                │                │  to_tsvector     │              │
  │                │                │─────────────────>│              │
  │                │<───────────────│ Resultados       │              │
  │<───────────────│                │                  │              │
  │                │                │                  │              │
  │ 9. Clica       │                │                  │              │
  │  em artigo     │                │                  │              │
  │───────────────>│ 10. GET        │                  │              │
  │                │  /knowledge/42 │                  │              │
  │                │───────────────>│                  │              │
  │                │                │ 11. SELECT +     │              │
  │                │                │  UPDATE          │              │
  │                │                │  view_count++    │              │
  │                │                │─────────────────>│              │
  │                │<───────────────│ Artigo completo  │              │
  │<───────────────│                │                  │              │
  │                │                │                  │              │
  │ 12. Lê artigo  │                │                  │              │
  │                │                │                  │              │
  │ 13. Problema   │                │                  │              │
  │     resolvido! │                │                  │              │
  │     Clica      │                │                  │              │
  │     "Útil"     │                │                  │              │
  │───────────────>│ 14. POST       │                  │              │
  │                │  /knowledge/42 │                  │              │
  │                │  /helpful      │                  │              │
  │                │───────────────>│ 15. UPDATE       │              │
  │                │                │  helpful_count++ │              │
  │                │                │─────────────────>│              │
  │                │<───────────────│ Obrigado!        │              │
  │<───────────────│                │                  │              │
```

---

## 4. Métricas e Analytics

### Métricas por Artigo:
```
- view_count: Quantas vezes foi visualizado
- helpful_count: Quantos clicaram "Útil"
- helpful_ratio: helpful_count / view_count
- last_viewed_at: Última visualização
```

### Métricas Globais:
```
- Artigos mais visualizados
- Artigos mais úteis
- Taxa de sucesso (helpful_ratio)
- Categorias mais acessadas
- Termos de busca populares (futuro)
```

---

## 5. Ciclo de Vida do Artigo

```
       [Rascunho]
            │
            │ Agente cria
            ▼
     ┌──────────────┐
     │  DRAFT       │
     │ (Não public.)│
     └──────┬───────┘
            │
            │ Agente publica
            ▼
     ┌──────────────┐
     │  PUBLISHED   │◄──────┐
     │ (Público)    │       │
     └──────┬───────┘       │
            │               │
            │ Admin         │ Admin
            │ despublica    │ republica
            ▼               │
     ┌──────────────┐       │
     │ UNPUBLISHED  │───────┘
     │ (Oculto)     │
     └──────────────┘
```

---

## 6. Busca Full-Text

### PostgreSQL Full-Text Search:

```sql
-- Índice GIN criado
CREATE INDEX idx_articles_content ON knowledge_articles
USING gin(to_tsvector('portuguese', content));

-- Query de busca
SELECT * FROM knowledge_articles
WHERE is_published = TRUE
AND to_tsvector('portuguese', title || ' ' || content)
  @@ to_tsquery('portuguese', 'senha & resetar');
```

### Ranking:
```sql
ORDER BY 
  ts_rank(to_tsvector('portuguese', content), query) DESC,
  view_count DESC
```

---

## 7. Cache Strategy

### Cached Queries:
```
- Lista de artigos por categoria (1h TTL)
- Artigo completo (1h TTL)
- Lista de categorias (24h TTL)
- Top 10 artigos (1h TTL)
```

### Cache Invalidation:
```
- Ao publicar artigo → invalidar lista
- Ao atualizar artigo → invalidar artigo
- Ao criar categoria → invalidar categorias
```

---

## 8. Organização

### Categorias Sugeridas:
- Conta e Login
- Configurações
- Pagamento e Cobrança
- Segurança
- Problemas Técnicos
- Tutoriais
- FAQ

### Tags Sugeridas:
- senha
- login
- email
- notificações
- pagamento
- perfil

---

## Decisões Arquiteturais Relacionadas
- [ADR 002: PostgreSQL Full-Text Search](../adr/002-uso-postgresql-database.md)
- [ADR 007: Redis Cache](../adr/007-redis-cache-chat.md)

---

**Versão**: 1.0
**Data**: 2024-12-07
**Autores**: Product Owner, Backend Developer

