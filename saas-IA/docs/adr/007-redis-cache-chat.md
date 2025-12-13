# ADR 007: Redis para Cache e Sessões de Chat

## Status
**Aceito** - 2024-12-07

## Decisores
- Backend Developer
- Database Engineer
- DevOps Engineer

## Contexto

O sistema de suporte ao cliente possui funcionalidades que se beneficiam de cache e armazenamento temporário:

- **Chat ao vivo**: Sessões ativas, presença de agentes online
- **Rate limiting**: Limitar tentativas de login
- **Cache de queries**: Artigos mais acessados, categorias
- **Session storage**: Dados temporários de usuário
- **Pub/Sub**: Notificações em tempo real (futuro)

### Requisitos:
- Armazenamento key-value rápido
- TTL (Time-To-Live) automático
- Suporte a estruturas de dados (lists, sets, hashes)
- Pub/Sub para mensageria (opcional)
- Performance sub-millisecond
- Persistência opcional

### Alternativas Consideradas:
1. **Redis** - In-memory data store
2. **Memcached** - Cache distribuído
3. **PostgreSQL** - Cache em tabelas do DB
4. **Sem cache** - Apenas PostgreSQL

## Decisão

Escolhemos **Redis 7** como solução de cache e armazenamento temporário.

### Justificativa:

**Vantagens do Redis:**
- **Performance**: Sub-millisecond latency
- **Estruturas de dados**: Strings, Lists, Sets, Hashes, Sorted Sets
- **TTL nativo**: Expiração automática de keys
- **Pub/Sub**: Mensageria para notificações real-time
- **Atomic operations**: INCR, DECR para rate limiting
- **Persistência opcional**: RDB snapshots, AOF log
- **Clustering**: Escalabilidade horizontal (futuro)
- **Maduro**: 15+ anos de desenvolvimento
- **Amplamente suportado**: Bibliotecas para todas linguagens

**Por que não Memcached:**
- Apenas strings (sem listas, sets, etc)
- Sem persistência
- Sem Pub/Sub
- Funcionalidades limitadas

**Por que não PostgreSQL para cache:**
- Performance inferior para cache
- Overhead de conexões SQL
- Não é para isso que foi projetado
- TTL requer cleanup manual

**Por que não "Sem cache":**
- Performance ruim em queries repetidas
- Sobrecarga no PostgreSQL
- Rate limiting complexo
- Chat ao vivo precisa de estado temporário

## Consequências

### Positivas:
- ✅ **Performance**: Cache reduz carga no PostgreSQL em 70%+
- ✅ **Chat ao vivo**: Estado de sessões em memória
- ✅ **Rate limiting**: Proteção contra brute force
- ✅ **Flexibilidade**: Múltiplas estruturas de dados
- ✅ **Pub/Sub ready**: Preparado para notificações
- ✅ **TTL automático**: Não precisa cleanup manual
- ✅ **Cloud-ready**: Disponível em Railway, Upstash, AWS

### Negativas:
- ⚠️ **Complexidade**: Mais um serviço para gerenciar
- ⚠️ **Memória**: Requer RAM dedicada
- ⚠️ **Volatilidade**: Dados perdidos se Redis cai (mas é cache)
- ⚠️ **Cache invalidation**: "One of the two hard problems in CS"

### Riscos Mitigados:
- Cache miss graceful: Fallback para PostgreSQL
- Persistência RDB para dados importantes
- Health checks no Docker Compose
- Logs para debugging
- Monitoring com redis-cli

## Casos de Uso

### 1. Cache de Queries Frequentes

**Problema**: Artigos da base de conhecimento consultados frequentemente

**Solução Redis:**
```python
# Buscar artigo
article_key = f"article:{article_id}"
cached = redis.get(article_key)

if cached:
    return json.loads(cached)

# Cache miss: buscar no PostgreSQL
article = db.query(KnowledgeArticle).get(article_id)

# Armazenar em cache (expira em 1 hora)
redis.setex(
    article_key,
    3600,  # TTL
    json.dumps(article.dict())
)

return article
```

**Benefício**: 90%+ dos requests servidos do cache

### 2. Sessões de Chat Ativas

**Problema**: Rastrear quais chats estão ativos e quais agentes estão online

**Solução Redis:**
```python
# Marcar agente como online
redis.sadd("agents:online", agent_id)
redis.expire(f"agent:{agent_id}:heartbeat", 60)

# Listar agentes online
online_agents = redis.smembers("agents:online")

# Chat ativo
redis.hset(f"chat:{chat_id}", mapping={
    "customer_id": customer_id,
    "agent_id": agent_id,
    "started_at": datetime.now().isoformat()
})
redis.expire(f"chat:{chat_id}", 3600)  # Expira em 1h
```

**Benefício**: Estado em tempo real sem polling do PostgreSQL

### 3. Rate Limiting (Anti-Brute Force)

**Problema**: Limitar tentativas de login para prevenir ataques

**Solução Redis:**
```python
# Login attempt
key = f"login:attempts:{email}"
attempts = redis.incr(key)

if attempts == 1:
    redis.expire(key, 300)  # Reset em 5 minutos

if attempts > 5:
    raise HTTPException(
        status_code=429,
        detail="Too many login attempts. Try again in 5 minutes."
    )
```

**Benefício**: Proteção contra brute force sem tabela no PostgreSQL

### 4. Cache de Contadores

**Problema**: Contador de visualizações em artigos atualizado a cada request

**Solução Redis:**
```python
# Incrementar views
redis.incr(f"article:{article_id}:views")

# A cada 100 views, sincronizar com PostgreSQL
if views % 100 == 0:
    article.view_count = redis.get(f"article:{article_id}:views")
    db.commit()
```

**Benefício**: Reduz writes no PostgreSQL em 99%

### 5. Pub/Sub para Notificações (Futuro)

**Problema**: Notificar agentes quando novo chat entra na fila

**Solução Redis:**
```python
# Publisher (quando novo chat criado)
redis.publish("new_chat_queue", json.dumps({
    "chat_id": chat_id,
    "customer_name": customer.name,
    "priority": "high"
}))

# Subscriber (agentes escutando)
pubsub = redis.pubsub()
pubsub.subscribe("new_chat_queue")

for message in pubsub.listen():
    notify_agents(message['data'])
```

**Benefício**: Notificações real-time sem WebSockets complexos

## Configuração

### docker-compose.yml:
```yaml
redis:
  image: redis:7-alpine
  ports:
    - "6379:6379"
  volumes:
    - redis_data:/data
  command: redis-server --appendonly yes
  healthcheck:
    test: ["CMD", "redis-cli", "ping"]
    interval: 10s
```

### Python (redis-py):
```python
import redis

redis_client = redis.from_url(
    settings.REDIS_URL,
    decode_responses=True,
    socket_timeout=5,
    socket_connect_timeout=5
)

# Verificar conexão
redis_client.ping()  # Returns True
```

## Estratégia de Cache

### Cache Patterns:

1. **Cache-Aside** (Lazy Loading):
   - Tenta buscar do cache
   - Se miss, busca do DB e popula cache
   - Usado para: artigos, categorias

2. **Write-Through**:
   - Escreve no cache e DB simultaneamente
   - Usado para: contadores críticos

3. **Write-Behind** (Delayed Write):
   - Escreve no cache imediatamente
   - Sincroniza com DB periodicamente
   - Usado para: view counts, analytics

### Cache Invalidation:

```python
# Ao atualizar artigo, invalidar cache
def update_article(article_id, data):
    # Atualizar DB
    article = db.query(KnowledgeArticle).get(article_id)
    article.update(data)
    db.commit()
    
    # Invalidar cache
    redis.delete(f"article:{article_id}")
```

## Performance

### Benchmarks esperados:
- **Cache hit**: < 1ms
- **Cache miss + DB**: 10-50ms
- **Rate limit check**: < 1ms
- **Session lookup**: < 1ms

### Cache hit ratio alvo: 80%+

## Alternativas Consideradas

| Solução | Prós | Contras | Decisão |
|---------|------|---------|---------|
| Redis | Rápido, versátil, Pub/Sub | Mais um serviço | ✅ Escolhido |
| Memcached | Simples, rápido | Limitado, sem Pub/Sub | ❌ Rejeitado |
| PostgreSQL | Já existe, persistente | Lento para cache | ❌ Rejeitado |
| Sem cache | Menos complexidade | Performance ruim | ❌ Rejeitado |

## Monitoring

### Métricas a monitorar:
- Hit rate: `INFO stats | grep keyspace_hits`
- Memory usage: `INFO memory`
- Connected clients: `INFO clients`
- Operations per second: `INFO stats | grep instantaneous_ops`

### Comandos úteis:
```bash
# Conectar ao Redis
redis-cli

# Ver todas keys
KEYS *

# Ver info do servidor
INFO

# Monitor em tempo real
MONITOR

# Flush cache (dev only)
FLUSHALL
```

## Referências
- [Redis Official Documentation](https://redis.io/docs/)
- [Redis Best Practices](https://redis.io/docs/manual/patterns/)
- [Cache Stampede Prevention](https://redis.io/docs/manual/patterns/cache-stampede/)

## Notas de Implementação
- Versão: Redis 7
- Client library: redis-py
- Persistência: AOF enabled
- Max memory: 256MB (development)
- Eviction policy: allkeys-lru
- Connection pooling: Enabled via redis-py

