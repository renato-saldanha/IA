# 📐 Documentação Arquitetural - SaaS de Suporte ao Cliente

## Bem-vindo!

Esta é a documentação arquitetural completa do projeto SaaS de Suporte ao Cliente. Aqui você encontrará decisões de design, diagramas e especificações técnicas detalhadas.

---

## 📋 Índice Rápido

- [ADRs (Architecture Decision Records)](#adrs)
- [Diagramas C4](#diagramas-c4)
- [Diagramas de Banco de Dados](#diagramas-de-banco-de-dados)
- [Diagramas de Fluxo](#diagramas-de-fluxo)
- [Guia de Leitura](#guia-de-leitura)

---

## 🎯 ADRs (Architecture Decision Records)

Documentos que explicam as principais decisões arquiteturais do projeto.

### Decisões de Stack

- **[ADR 001: Escolha do FastAPI como Backend](adr/001-escolha-fastapi-backend.md)**
  - Por que FastAPI vs Flask/Django
  - Performance, async, documentação automática
  
- **[ADR 002: PostgreSQL como Banco de Dados](adr/002-uso-postgresql-database.md)**
  - Por que PostgreSQL vs MySQL/MongoDB
  - ACID, full-text search, tipos ricos

- **[ADR 005: Next.js com App Router para Frontend](adr/005-frontend-nextjs-typescript.md)**
  - Por que Next.js vs CRA/Vite
  - SSR, performance, developer experience

### Decisões de Segurança e Infraestrutura

- **[ADR 003: Autenticação JWT](adr/003-autenticacao-jwt.md)**
  - Por que JWT vs sessions/OAuth2
  - Stateless, escalável, padrão da indústria

- **[ADR 004: Containerização com Docker](adr/004-containerizacao-docker.md)**
  - Por que Docker Compose vs Kubernetes/VMs
  - Simplicidade, portabilidade, reprodutibilidade

- **[ADR 007: Redis para Cache e Chat](adr/007-redis-cache-chat.md)**
  - Por que Redis vs Memcached/PostgreSQL
  - Performance, estruturas de dados, Pub/Sub

### Decisões de Organização

- **[ADR 006: Estrutura Modular do Backend](adr/006-estrutura-modular-backend.md)**
  - Clean Architecture com camadas
  - API, Core, Models, Schemas, DB

- **[ADR 008: Tailwind CSS para Estilização](adr/008-tailwind-css-styling.md)**
  - Por que Tailwind vs CSS Modules/Styled Components
  - Velocidade, consistência, performance

---

## 🏗️ Diagramas C4

Modelos C4 mostrando a arquitetura do sistema em diferentes níveis de detalhe.

### Level 1: Context (Visão Geral)

- **[C4 Level 1: Context Diagram](architecture/c4-level1-context.md)**
  - Sistema e seus usuários
  - Atores: Cliente, Agente, Admin
  - Sistemas externos (SMTP)
  - Scope do projeto

### Level 2: Containers (Aplicações)

- **[C4 Level 2: Containers Diagram](architecture/c4-level2-containers.md)**
  - Frontend (Next.js)
  - Backend (FastAPI)
  - PostgreSQL Database
  - Redis Cache
  - Comunicação entre containers

### Level 3: Components (Internos)

- **[C4 Level 3: Backend Components](architecture/c4-level3-components-backend.md)**
  - API Layer (routers, dependencies)
  - Core Layer (config, security)
  - Schemas Layer (Pydantic DTOs)
  - Models Layer (SQLAlchemy)
  - Database Layer (session management)

- **[C4 Level 3: Frontend Components](architecture/c4-level3-components-frontend.md)**
  - App Router (pages, layouts)
  - Components Layer (UI, forms)
  - Library Layer (API client, types)
  - Styling Layer (Tailwind)

---

## 🗄️ Diagramas de Banco de Dados

Modelagem completa do banco de dados PostgreSQL.

- **[Diagrama ER (Entity-Relationship)](diagrams/database-er-diagram.md)**
  - 5 entidades principais
  - Relacionamentos (1:N, N:M)
  - Campos, tipos e constraints
  - Enums (UserRole, TicketStatus, etc)
  - Volumes de dados estimados

- **[Estratégia de Índices](diagrams/database-indexes.md)**
  - Índices B-tree (FKs, filters)
  - Índices GIN (full-text search)
  - Índices BRIN (timestamps)
  - Performance targets
  - Trade-offs e manutenção

---

## 🔄 Diagramas de Fluxo

Fluxos principais do sistema com diagramas de sequência.

- **[Fluxo de Autenticação](diagrams/authentication-flow.md)**
  - Registro de usuário
  - Login com JWT
  - Requests autenticados
  - Logout
  - Error handling

- **[Ciclo de Vida do Ticket](diagrams/ticket-lifecycle.md)**
  - Estados: Open → In Progress → Resolved → Closed
  - Transições permitidas
  - Regras de negócio
  - Permissões por role
  - SLAs (planejado)

- **[Diagrama de Sequência: Chat](diagrams/chat-sequence-diagram.md)**
  - Iniciação (waiting)
  - Aceitação por agente (active)
  - Troca de mensagens (polling)
  - Finalização (ended)
  - Avaliação

- **[Fluxo da Base de Conhecimento](diagrams/knowledge-base-flow.md)**
  - Criação de artigo
  - Publicação
  - Busca full-text
  - Métricas (views, helpful)
  - Cache strategy

---

## 📖 Guia de Leitura

### Para Novos Desenvolvedores

**Ordem recomendada:**

1. Comece pelo contexto: [C4 Level 1: Context](architecture/c4-level1-context.md)
2. Entenda os containers: [C4 Level 2: Containers](architecture/c4-level2-containers.md)
3. Veja o banco de dados: [Diagrama ER](diagrams/database-er-diagram.md)
4. Estude os componentes do seu time:
   - Backend: [C4 Level 3: Backend](architecture/c4-level3-components-backend.md)
   - Frontend: [C4 Level 3: Frontend](architecture/c4-level3-components-frontend.md)
5. Leia ADRs relevantes conforme necessário

**Tempo estimado:** 2-3 horas

---

### Para Tech Leads / Arquitetos

**Ordem recomendada:**

1. Revise todos os ADRs: [ADRs completos](#adrs)
2. Analise a estrutura completa: [C4 Level 2](architecture/c4-level2-containers.md)
3. Valide decisões de banco: [ER Diagram](diagrams/database-er-diagram.md) + [Índices](diagrams/database-indexes.md)
4. Revise fluxos críticos: [Todos os diagramas de fluxo](#diagramas-de-fluxo)

**Tempo estimado:** 4-5 horas

---

### Para DBAs / Database Engineers

**Ordem recomendada:**

1. Modelagem: [Diagrama ER](diagrams/database-er-diagram.md)
2. Performance: [Estratégia de Índices](diagrams/database-indexes.md)
3. Decisão de DB: [ADR 002: PostgreSQL](adr/002-uso-postgresql-database.md)
4. Cache: [ADR 007: Redis](adr/007-redis-cache-chat.md)

**Tempo estimado:** 1-2 horas

---

### Para Security Engineers

**Ordem recomendada:**

1. Autenticação: [ADR 003: JWT](adr/003-autenticacao-jwt.md)
2. Fluxo de auth: [Diagrama de Autenticação](diagrams/authentication-flow.md)
3. Infraestrutura: [ADR 004: Docker](adr/004-containerizacao-docker.md)
4. Componentes backend: [C4 Level 3: Backend](architecture/c4-level3-components-backend.md)

**Tempo estimado:** 2 horas

---

### Para Product Owners / PMs

**Ordem recomendada:**

1. Visão geral: [C4 Level 1: Context](architecture/c4-level1-context.md)
2. Fluxo de tickets: [Ticket Lifecycle](diagrams/ticket-lifecycle.md)
3. Fluxo de chat: [Chat Sequence](diagrams/chat-sequence-diagram.md)
4. Base de conhecimento: [KB Flow](diagrams/knowledge-base-flow.md)

**Tempo estimado:** 1 hora

---

## 🔍 Busca Rápida

### "Onde está documentado...?"

| Busco por... | Documento |
|-------------|-----------|
| Por que FastAPI? | [ADR 001](adr/001-escolha-fastapi-backend.md) |
| Como funciona o login? | [Auth Flow](diagrams/authentication-flow.md) |
| Estrutura do banco? | [ER Diagram](diagrams/database-er-diagram.md) |
| Como funciona o chat? | [Chat Sequence](diagrams/chat-sequence-diagram.md) |
| Estados do ticket? | [Ticket Lifecycle](diagrams/ticket-lifecycle.md) |
| Estrutura do backend? | [Backend Components](architecture/c4-level3-components-backend.md) |
| Estrutura do frontend? | [Frontend Components](architecture/c4-level3-components-frontend.md) |
| Por que Docker? | [ADR 004](adr/004-containerizacao-docker.md) |
| Estratégia de cache? | [ADR 007](adr/007-redis-cache-chat.md) |
| Índices do banco? | [Database Indexes](diagrams/database-indexes.md) |

---

## 📊 Estatísticas da Documentação

- **ADRs**: 8 documentos
- **Diagramas C4**: 4 documentos (3 níveis)
- **Diagramas de DB**: 2 documentos
- **Diagramas de Fluxo**: 4 documentos
- **Total**: 18 documentos arquiteturais
- **Páginas estimadas**: ~80 páginas
- **Tempo de leitura completo**: 6-8 horas

---

## 🎓 Convenções

### Formato dos Documentos

Todos os documentos seguem estrutura consistente:
- Descrição clara no início
- Diagramas visuais (ASCII art)
- Justificativas detalhadas
- Trade-offs explícitos
- Decisões vs alternativas
- Links para documentos relacionados
- Versão e autores

### Versionamento

- Todos documentos têm versão (1.0 inicial)
- Data de criação registrada
- Autores identificados

---

## 🔄 Mantendo Atualizado

### Quando atualizar:

- ✅ Nova decisão arquitetural → Criar novo ADR
- ✅ Mudança de fluxo → Atualizar diagrama
- ✅ Nova entidade no banco → Atualizar ER
- ✅ Novo índice → Atualizar doc de índices
- ✅ Mudança de stack → Atualizar ADR + C4

### Processo:

1. Editar documento Markdown
2. Atualizar versão (1.0 → 1.1)
3. Adicionar nota de changelog
4. Commitar com mensagem descritiva

---

## 🤝 Contribuindo

Para adicionar/atualizar documentação:

1. Siga o formato dos documentos existentes
2. Use diagramas ASCII para visualização
3. Explique o "porquê", não apenas o "o quê"
4. Liste sempre alternativas consideradas
5. Documente trade-offs
6. Adicione links para docs relacionados

---

## 📞 Contato

Dúvidas sobre arquitetura:
- Tech Lead: (ver README principal)
- Software Architect: (ver README principal)

---

## 🔗 Links Relacionados

- [README Principal](../README.md)
- [Guia de Início Rápido](../GUIA_INICIO_RAPIDO.md)
- [API Docs](../API_DOCS.md)
- [Setup Windows](../WINDOWS_SETUP.md)

---

**Última atualização**: 2024-12-07
**Versão da documentação**: 1.0
**Mantenedores**: Tech Lead, Software Architect

---

*"Good architecture is not the most beautiful one, but the one that solves the problem."*

