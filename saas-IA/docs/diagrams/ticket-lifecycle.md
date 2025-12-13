# Ciclo de Vida do Ticket - Fluxo Completo

## Descrição
Diagrama mostrando todos os estados possíveis de um ticket e as transições entre eles.

---

## Diagrama de Estados

```
                              [CRIAÇÃO]
                                  │
                                  ▼
                           ┌────────────┐
                           │    OPEN    │◄────┐
                           │  (Aberto)  │     │
                           └──────┬─────┘     │
                                  │           │
                    Agente aceita │           │ Cliente reabre
                                  │           │ ou nova mensagem
                                  ▼           │
                           ┌────────────────┐ │
                           │  IN_PROGRESS   │ │
                           │ (Em Progresso) │ │
                           └────┬──────┬────┘ │
                                │      │      │
              Aguarda cliente   │      │ Agente resolve
                                │      │      │
                                ▼      ▼      │
                    ┌──────────┐  ┌──────────┐│
                    │ WAITING  │  │ RESOLVED ││
                    │(Aguard.) │  │(Resolv.) ││
                    └────┬─────┘  └────┬─────┘│
                         │             │      │
                         │             │Cliente│
                         │Agente volta │reabré│
                         └─────────────┴──────┘
                                  │
                         Cliente/Admin fecha
                                  ▼
                           ┌────────────┐
                           │   CLOSED   │
                           │ (Fechado)  │
                           └────────────┘
                              [FINAL]
```

---

## Estados

| Status | Descrição | Quem pode transicionar |
|--------|-----------|------------------------|
| **OPEN** | Ticket acabou de ser criado ou reaberto | Sistema, Cliente |
| **IN_PROGRESS** | Agente está trabalhando no ticket | Agente, Admin |
| **WAITING** | Aguardando resposta do cliente | Agente, Admin |
| **RESOLVED** | Problema resolvido, aguarda confirmação | Agente, Admin |
| **CLOSED** | Ticket finalizado | Cliente, Admin |

---

## Transições Permitidas

### 1. OPEN → IN_PROGRESS
**Trigger**: Agente aceita o ticket ou adiciona primeira resposta
**Ação**: `assigned_to = agent_id`

### 2. IN_PROGRESS → WAITING
**Trigger**: Agente solicita informações do cliente
**Ação**: Notificar cliente (futuro)

### 3. IN_PROGRESS → RESOLVED
**Trigger**: Agente marca como resolvido
**Ação**: `resolved_at = now()`

### 4. WAITING → IN_PROGRESS
**Trigger**: Cliente responde

### 5. RESOLVED → CLOSED
**Trigger**: Cliente confirma ou auto-close após 7 dias (futuro)
**Ação**: `closed_at = now()`

### 6. RESOLVED → OPEN
**Trigger**: Cliente reabré (problema não resolvido)

### 7. WAITING/IN_PROGRESS → OPEN
**Trigger**: Reatribuição ou cliente adiciona mensagem

---

## Fluxo Típico Bem-Sucedido

```
1. Cliente cria ticket → OPEN
2. Agente aceita → IN_PROGRESS
3. Agente resolve → RESOLVED
4. Cliente confirma → CLOSED
```

**Tempo médio**: 2-3 dias

---

## Fluxo com Complicações

```
1. Cliente cria ticket → OPEN
2. Agente aceita → IN_PROGRESS
3. Agente precisa de info → WAITING
4. Cliente responde → IN_PROGRESS
5. Agente resolve → RESOLVED
6. Cliente não confirma → Auto-close → CLOSED (7 dias)
```

---

## Fluxo de Reabertura

```
1. Ticket em RESOLVED
2. Cliente testa solução
3. Problema persiste
4. Cliente reabre → OPEN
5. Agente revisa → IN_PROGRESS
```

---

## Regras de Negócio

### Permissões por Role

| Ação | Cliente | Agente | Admin |
|------|---------|--------|-------|
| Criar ticket | ✅ | ✅ | ✅ |
| Ver próprios tickets | ✅ | ❌ | ❌ |
| Ver todos tickets | ❌ | ✅ | ✅ |
| Aceitar ticket | ❌ | ✅ | ✅ |
| Mudar status | ❌ | ✅ | ✅ |
| Reabrir resolvido | ✅ | ✅ | ✅ |
| Deletar ticket | ❌ | ❌ | ✅ |
| Ver notas internas | ❌ | ✅ | ✅ |

### SLA (Planejado v2.0)

| Prioridade | Primeira Resposta | Resolução |
|------------|-------------------|-----------|
| Urgent | 1 hora | 4 horas |
| High | 4 horas | 24 horas |
| Medium | 12 horas | 3 dias |
| Low | 24 horas | 7 dias |

---

## Métricas

### Por Ticket:
- Tempo até primeira resposta
- Tempo até resolução
- Número de mensagens
- Número de reaberturas

### Globais:
- Taxa de resolução na primeira tentativa
- Tempo médio de resolução
- Tickets por agente
- Satisfação do cliente (futuro)

---

## Decisões Arquiteturais Relacionadas
- [ADR 001: FastAPI Backend](../adr/001-escolha-fastapi-backend.md)
- [ADR 002: PostgreSQL Database](../adr/002-uso-postgresql-database.md)

---

**Versão**: 1.0
**Data**: 2024-12-07
**Autores**: Product Owner, Backend Developer

