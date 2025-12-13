# C4 Model - Level 1: Context Diagram

## Sistema de Suporte ao Cliente - Visão de Contexto

### Descrição
Este diagrama mostra o sistema de suporte ao cliente e como ele interage com usuários e sistemas externos em um nível alto.

---

## Diagrama

```
                                    ┌─────────────────────┐
                                    │                     │
                                    │   Admin Sistema     │
                                    │   (Pessoa)          │
                                    │                     │
                                    └──────────┬──────────┘
                                               │
                                               │ Gerencia usuários,
                                               │ configura sistema,
                                               │ visualiza métricas
                                               │
                ┌─────────────────┐            ▼
                │                 │   ┌────────────────────────┐
                │  Cliente        │   │                        │
                │  (Pessoa)       │──▶│   Sistema de Suporte   │
                │                 │   │   ao Cliente           │
                └─────────────────┘   │   [Software System]    │
                                      │                        │
                  Cria tickets,       │  - Help Desk (Tickets) │
                  inicia chats,       │  - Chat ao Vivo        │
                  busca artigos       │  - Base de Conhecimento│
                                      │  - Autenticação JWT    │
                ┌─────────────────┐   │                        │
                │                 │   └────────────┬───────────┘
                │ Agente Suporte  │                │
                │ (Pessoa)        │◀───────────────┘
                │                 │
                └─────────────────┘   Envia emails
                                      de notificação
                  Responde tickets,   (opcional)
                  aceita chats,              │
                  cria artigos               ▼
                                      ┌──────────────┐
                                      │              │
                                      │   Servidor   │
                                      │   SMTP       │
                                      │   [External] │
                                      │              │
                                      └──────────────┘
```

---

## Atores

### 1. Cliente (Customer)
**Tipo**: Pessoa
**Descrição**: Usuário final que precisa de suporte

**Ações principais:**
- Criar tickets de suporte
- Enviar mensagens em tickets
- Iniciar sessões de chat ao vivo
- Buscar e visualizar artigos da base de conhecimento
- Avaliar artigos e atendimentos

**Objetivos:**
- Resolver problemas rapidamente
- Obter respostas para dúvidas
- Acessar documentação de autoatendimento

---

### 2. Agente de Suporte (Support Agent)
**Tipo**: Pessoa
**Descrição**: Profissional que atende clientes

**Ações principais:**
- Visualizar e gerenciar tickets atribuídos
- Responder mensagens em tickets
- Aceitar e atender chats da fila
- Criar e publicar artigos na base de conhecimento
- Adicionar notas internas

**Objetivos:**
- Atender clientes eficientemente
- Resolver tickets rapidamente
- Documentar soluções comuns
- Colaborar com outros agentes

---

### 3. Administrador (Admin)
**Tipo**: Pessoa
**Descrição**: Gestor do sistema

**Ações principais:**
- Gerenciar usuários (criar, editar, desativar)
- Configurar categorias e prioridades
- Visualizar métricas e relatórios
- Deletar tickets e artigos
- Gerenciar permissões

**Objetivos:**
- Manter sistema funcionando
- Gerenciar equipe de suporte
- Monitorar performance
- Garantir qualidade do atendimento

---

## Sistema

### Sistema de Suporte ao Cliente
**Tipo**: Software System
**Tecnologia**: Next.js (Frontend) + FastAPI (Backend)
**Descrição**: Plataforma completa de suporte ao cliente

**Funcionalidades principais:**

1. **Help Desk (Sistema de Tickets)**
   - Criação e gerenciamento de tickets
   - Sistema de prioridades e status
   - Atribuição automática e manual
   - Histórico completo de interações

2. **Chat ao Vivo**
   - Sessões de chat em tempo real
   - Fila de espera para clientes
   - Sistema de aceitação por agentes
   - Avaliação de atendimento

3. **Base de Conhecimento**
   - Portal de artigos e FAQs
   - Busca full-text
   - Categorização e tags
   - Métricas de utilidade

4. **Autenticação e Autorização**
   - Login com JWT
   - Três níveis de acesso (Cliente, Agente, Admin)
   - Controle de permissões por role

---

## Sistemas Externos

### Servidor SMTP (Opcional)
**Tipo**: External System
**Descrição**: Servidor de email para notificações

**Uso:**
- Notificar clientes sobre atualizações de tickets
- Alertar agentes sobre novos tickets
- Enviar relatórios periódicos para admins
- Notificações de senha resetada

**Status**: Planejado (não implementado na v1.0)

---

## Fluxos Principais

### Fluxo 1: Cliente cria ticket
```
Cliente → Sistema → Ticket criado → (Email opcional) → Agente notificado
```

### Fluxo 2: Chat ao vivo
```
Cliente inicia chat → Sistema (fila) → Agente aceita → Conversa → Avaliação
```

### Fluxo 3: Busca na base de conhecimento
```
Cliente busca → Sistema consulta → Resultados → Cliente visualiza → Métricas
```

### Fluxo 4: Agente responde ticket
```
Agente visualiza → Escreve resposta → Sistema atualiza → Cliente notificado
```

---

## Contexto Técnico

### Deployment:
- **Frontend**: Vercel (Edge Network)
- **Backend**: Railway / Render
- **Database**: PostgreSQL (managed)
- **Cache**: Redis (managed)

### Integrações Futuras:
- WhatsApp Business API
- Telegram Bot
- Slack Integration
- Email (SMTP/SendGrid)
- Analytics (Google Analytics, Mixpanel)

---

## Requisitos Não Funcionais

### Performance:
- Resposta de API < 200ms
- Chat latência < 1s
- Disponibilidade: 99.9%

### Segurança:
- HTTPS obrigatório
- JWT com expiração
- Senhas hasheadas (bcrypt)
- Rate limiting

### Escalabilidade:
- Suporte a 1.000+ usuários simultâneos
- 10.000+ tickets por mês
- 100+ chats simultâneos

---

## Escopo

### O que ESTÁ no escopo:
✅ Help desk com tickets
✅ Chat ao vivo
✅ Base de conhecimento
✅ Autenticação JWT
✅ Three-tier user roles
✅ Responsive web interface

### O que NÃO está no escopo (v1.0):
❌ Aplicativo mobile nativo
❌ Integração com WhatsApp/Telegram
❌ Chatbot com IA
❌ Videochamadas
❌ Integração com CRM externo
❌ API pública para third-party

---

## Decisões Arquiteturais Relacionadas
- [ADR 001: FastAPI Backend](../adr/001-escolha-fastapi-backend.md)
- [ADR 003: Autenticação JWT](../adr/003-autenticacao-jwt.md)
- [ADR 005: Next.js Frontend](../adr/005-frontend-nextjs-typescript.md)

---

**Versão**: 1.0
**Data**: 2024-12-07
**Autores**: Tech Lead, Software Architect

