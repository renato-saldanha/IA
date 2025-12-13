# ADR 002: Uso do PostgreSQL como Banco de Dados Principal

## Status
**Aceito** - 2024-12-07

## Decisores
- Database Engineer
- Tech Lead
- Backend Developer

## Contexto

O sistema de suporte ao cliente requer armazenamento persistente para usuários, tickets, mensagens, sessões de chat e artigos da base de conhecimento. Precisamos de um banco de dados que suporte:

- Relacionamentos complexos entre entidades (1:N, N:M)
- Transações ACID para integridade de dados
- Busca full-text em artigos e tickets
- Índices para queries rápidas
- Escalabilidade vertical e horizontal
- Suporte a JSON para dados semi-estruturados (opcional)

### Alternativas Consideradas:
1. **PostgreSQL** - Banco relacional open-source robusto
2. **MySQL** - Banco relacional popular
3. **MongoDB** - Banco de dados NoSQL orientado a documentos
4. **SQLite** - Banco de dados embutido

## Decisão

Escolhemos **PostgreSQL 16** como banco de dados principal.

### Justificativa:

**Vantagens do PostgreSQL:**
- **ACID completo**: Garante integridade transacional crítica para tickets e mensagens
- **Tipos de dados ricos**: JSON, ARRAY, ENUM nativos
- **Full-text search**: Busca nativa em texto sem necessidade de Elasticsearch
- **Índices avançados**: B-tree, GIN, GIST, BRIN para otimização
- **Extensibilidade**: pg_trgm para fuzzy search, PostGIS se necessário
- **Performance**: Excelente para leituras e escritas complexas
- **Maturidade**: 30+ anos de desenvolvimento
- **Conformidade SQL**: Segue padrões SQL rigorosamente
- **Open source**: Licença permissiva

**Por que não MySQL:**
- Menor suporte a tipos de dados avançados
- Full-text search menos robusto
- Histórico de problemas com transações em versões antigas
- Índices menos flexíveis

**Por que não MongoDB:**
- Modelo de dados do sistema é fortemente relacional
- Relacionamentos entre User ↔ Ticket ↔ Message são fundamentais
- ACID em múltiplas coleções é complexo
- Queries JOIN seriam problemáticas
- Overhead de desnormalização não justificado

**Por que não SQLite:**
- Não suporta múltiplas conexões de escrita simultâneas
- Sem recursos de replicação nativa
- Não adequado para produção com múltiplos workers

## Consequências

### Positivas:
- ✅ **Integridade de dados**: ACID garante consistência em tickets e mensagens
- ✅ **Busca full-text**: Artigos da base de conhecimento com busca nativa
- ✅ **Escalabilidade**: Replicação read-replica para escalar leituras
- ✅ **JSON support**: Campos flexíveis quando necessário (metadata, configs)
- ✅ **Ferramentas maduras**: pgAdmin, DBeaver, múltiplas opções de backup
- ✅ **Cloud-ready**: Suporte em todos provedores (AWS RDS, Railway, Render)
- ✅ **ORMs excelentes**: SQLAlchemy tem suporte excepcional para PostgreSQL

### Negativas:
- ⚠️ **Complexidade inicial**: Setup mais complexo que SQLite
- ⚠️ **Recursos**: Requer mais memória que bancos mais simples
- ⚠️ **Curva de aprendizado**: SQL e otimizações requerem conhecimento

### Riscos Mitigados:
- Alembic para migrations versionadas
- Backups automáticos em produção
- Monitoring com pgAdmin/DataDog
- Índices bem planejados desde o início

## Schema Design

### Tabelas Principais:
- `users` - Usuários do sistema (clientes, agentes, admins)
- `tickets` - Tickets de suporte
- `messages` - Mensagens de tickets e chats
- `chat_sessions` - Sessões de chat ao vivo
- `knowledge_articles` - Artigos da base de conhecimento

### Índices Planejados:
- B-tree em chaves estrangeiras (user_id, ticket_id, etc)
- GIN para full-text search em artigos
- BRIN para timestamps (created_at, updated_at)
- Índices compostos para queries frequentes

## Alternativas Consideradas

| Banco | Prós | Contras | Decisão |
|-------|------|---------|---------|
| PostgreSQL | ACID, full-text, tipos ricos | Mais recursos, complexo | ✅ Escolhido |
| MySQL | Popular, simples | Menos features, FTS fraco | ❌ Rejeitado |
| MongoDB | Flexível, escala horizontal | Não relacional, sem JOINs | ❌ Rejeitado |
| SQLite | Simples, zero config | Single-user, sem replica | ❌ Rejeitado |

## Configurações de Produção

```yaml
PostgreSQL 16:
  - max_connections: 100
  - shared_buffers: 256MB
  - effective_cache_size: 1GB
  - work_mem: 4MB
  - maintenance_work_mem: 64MB
  - checkpoint_completion_target: 0.9
  - wal_buffers: 16MB
```

## Referências
- [PostgreSQL Official Documentation](https://www.postgresql.org/docs/)
- [PostgreSQL Full-Text Search](https://www.postgresql.org/docs/current/textsearch.html)
- [SQLAlchemy with PostgreSQL](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html)

## Notas de Implementação
- Versão: PostgreSQL 16
- Container: Official postgres:16-alpine image
- Connection pooling via SQLAlchemy
- Migrations: Alembic
- Extensions utilizadas: pg_trgm (fuzzy search)

