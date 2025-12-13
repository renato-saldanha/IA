# Diagrama de Sequência - Chat ao Vivo

## Descrição
Fluxo completo de uma sessão de chat ao vivo, desde iniciação até finalização.

---

## Diagrama de Sequência

```
Cliente          Frontend         Backend          PostgreSQL       Redis
  │                │                │                  │              │
  │ 1. Clica       │                │                  │              │
  │ "Iniciar Chat" │                │                  │              │
  │───────────────>│                │                  │              │
  │                │ 2. POST /chats/│                  │              │
  │                │───────────────>│                  │              │
  │                │                │ 3. INSERT        │              │
  │                │                │  chat_session    │              │
  │                │                │─────────────────>│              │
  │                │                │                  │ 4. Cache     │
  │                │                │  chat:waiting    │              │
  │                │                │─────────────────────────────────>│
  │                │<───────────────│ 201 Created      │              │
  │<───────────────│ session_id     │                  │              │
  │                │                │                  │              │
  │ 5. Aguarda     │ 6. Polling     │                  │              │
  │    atendimento │    /chats/{id} │                  │              │
  │                │───────────────>│                  │              │
  │                │<───────────────│ status:waiting   │              │
  │                │                │                  │              │
                            [AGENTE ENTRA]
                                    │                  │              │
Agente                              │ 7. GET           │              │
  │                                 │  /chats/waiting  │              │
  │                                 │<─────────────────┤              │
  │                                 │ Lista de espera  │              │
  │ 8. Aceita chat                  │                  │              │
  │────────────────────────────────>│                  │              │
  │                                 │ 9. UPDATE        │              │
  │                                 │  agent_id, status│              │
  │                                 │─────────────────>│              │
  │                                 │                  │ 10. Cache    │
  │                                 │  chat:active     │              │
  │                                 │─────────────────────────────────>│
  │<────────────────────────────────│ Chat aceito      │              │
  │                                 │                  │              │
Cliente                             │                  │              │
  │ 11. Notificado                  │                  │              │
  │<────────────────────────────────│                  │              │
  │                                 │                  │              │
  │ 12. Envia msg                   │                  │              │
  │────────────────────────────────>│ 13. INSERT msg   │              │
  │                                 │─────────────────>│              │
  │                                 │                  │              │
Agente                              │                  │              │
  │ 14. Polling                     │                  │              │
  │   /chats/{id}/messages          │                  │              │
  │────────────────────────────────>│ 15. SELECT msgs  │              │
  │                                 │─────────────────>│              │
  │<────────────────────────────────│ Novas mensagens  │              │
  │                                 │                  │              │
  │ 16. Responde                    │                  │              │
  │────────────────────────────────>│ 17. INSERT msg   │              │
  │                                 │─────────────────>│              │
  │                                 │                  │              │
Cliente                             │                  │              │
  │ 18. Polling                     │                  │              │
  │────────────────────────────────>│                  │              │
  │<────────────────────────────────│ Resposta agente  │              │
  │                                 │                  │              │
              [CONVERSA CONTINUA...]
                                    │                  │              │
Agente ou Cliente                   │                  │              │
  │ 19. Finaliza chat               │                  │              │
  │────────────────────────────────>│ 20. UPDATE       │              │
  │                                 │  status=ended,   │              │
  │                                 │  ended_at        │              │
  │                                 │─────────────────>│              │
  │                                 │                  │ 21. Delete   │
  │                                 │  from cache      │              │
  │                                 │─────────────────────────────────>│
  │<────────────────────────────────│ Chat finalizado  │              │
  │                                 │                  │              │
Cliente                             │                  │              │
  │ 22. Avalia                      │                  │              │
  │     atendimento                 │                  │              │
  │────────────────────────────────>│ 23. UPDATE       │              │
  │                                 │  rating, feedback│              │
  │                                 │─────────────────>│              │
  │<────────────────────────────────│ Obrigado!        │              │
```

---

## Fases do Chat

### Fase 1: Iniciação (Waiting)
- Cliente cria sessão
- Status = WAITING
- Entra na fila (Redis)

### Fase 2: Aceitação (Active)
- Agente vê fila
- Aceita chat
- Status = ACTIVE
- Cliente notificado

### Fase 3: Conversa (Active)
- Troca de mensagens
- Polling a cada 2-3s
- Mensagens em PostgreSQL

### Fase 4: Finalização (Ended)
- Qualquer parte encerra
- Status = ENDED
- ended_at registrado

### Fase 5: Avaliação (Opcional)
- Cliente avalia (1-5 estrelas)
- Feedback opcional

---

## Tempo Real (v1.0)

### Polling Strategy:
```javascript
// Frontend
setInterval(async () => {
  const messages = await apiClient.getChatMessages(sessionId)
  setMessages(messages)
}, 3000) // Poll a cada 3 segundos
```

### Futuro: WebSockets (v2.0)
```javascript
// Socket.io ou WebSocket nativo
socket.on('new_message', (message) => {
  appendMessage(message)
})
```

---

## Estados da Sessão

| Status | Descrição | Cliente | Agente |
|--------|-----------|---------|--------|
| WAITING | Aguardando agente | Vê "Aguardando..." | Vê na fila |
| ACTIVE | Conversação ativa | Pode enviar msgs | Pode enviar msgs |
| ENDED | Finalizado | Pode avaliar | Pode ver histórico |

---

## Decisões Arquiteturais Relacionadas
- [ADR 007: Redis Cache](../adr/007-redis-cache-chat.md)

---

**Versão**: 1.0
**Data**: 2024-12-07
**Autores**: Backend Developer, Frontend Developer

