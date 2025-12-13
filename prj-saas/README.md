# SaaS de Suporte ao Cliente

Sistema completo de help desk com chat ao vivo, gerenciamento de tickets e base de conhecimento.

## 🚀 Tecnologias

### Backend
- **FastAPI** - Framework web moderno e rápido
- **SQLModel** - ORM baseado em Pydantic e SQLAlchemy
- **PostgreSQL** - Banco de dados relacional
- **Redis** - Cache e sessões
- **JWT** - Autenticação segura

### Frontend
- **Next.js 15** - Framework React com SSR/SSG
- **Tailwind CSS** - Estilização utility-first
- **shadcn/ui** - Componentes UI modernos
- **Axios** - Cliente HTTP

### Infraestrutura
- **Docker & Docker Compose** - Containerização
- **Alembic** - Migrações de banco de dados

## 📋 Funcionalidades

### ✅ Help Desk
- Criação e gerenciamento de tickets
- Priorização (baixa, média, alta, urgente)
- Status (aberto, em progresso, aguardando, resolvido, fechado)
- Atribuição a agentes
- Filtros e busca
- Tags personalizadas

### 💬 Sistema de Mensagens
- Histórico completo por ticket
- Mensagens internas (apenas para equipe)
- Suporte a múltiplos canais (email, chat, formulário, widget)

### 📚 Base de Conhecimento
- Artigos e FAQs
- Categorização
- Busca full-text
- Controle de publicação
- Contador de visualizações
- Portal público de autoatendimento

### 👥 Gestão de Usuários
- Autenticação JWT (access + refresh tokens)
- Roles: Admin, Agent, Customer
- Multi-tenancy (organizações)
- RBAC por organização

## 🏗️ Estrutura do Projeto

```
prj/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── deps.py           # Dependências de auth
│   │   │   └── v1/
│   │   │       ├── auth.py       # Rotas de autenticação
│   │   │       ├── tickets.py    # Rotas de tickets
│   │   │       ├── knowledge.py  # Rotas de conhecimento
│   │   │       └── router.py     # Router principal
│   │   ├── core/
│   │   │   ├── config.py         # Configurações
│   │   │   └── security.py       # JWT e hashing
│   │   ├── db/
│   │   │   └── session.py        # Sessão do banco
│   │   ├── models/
│   │   │   └── models.py         # Modelos SQLModel
│   │   └── schemas/
│   │       └── schemas.py        # Schemas Pydantic
│   ├── main.py                   # Aplicação FastAPI
│   └── requirements.txt
│
├── frontend/
│   ├── app/
│   │   ├── layout.tsx            # Layout principal
│   │   ├── page.tsx              # Página inicial
│   │   └── globals.css           # Estilos globais
│   ├── lib/
│   │   ├── api.ts                # Cliente HTTP
│   │   └── types.ts              # TypeScript types
│   ├── package.json
│   ├── tailwind.config.ts
│   └── tsconfig.json
│
├── docker/
│   ├── Dockerfile.backend
│   └── Dockerfile.frontend
│
└── docker-compose.yml
```

## 🚀 Como Rodar

### Pré-requisitos
- Docker e Docker Compose
- (Opcional) Node.js 20+ e Python 3.11+ para desenvolvimento local

### Com Docker Compose (Recomendado)

1. Clone o repositório e navegue até a pasta:
```bash
cd prj
```

2. (Opcional) Crie um arquivo `.env` na raiz:
```bash
SECRET_KEY=your-super-secret-key-here
```

3. Inicie os serviços:
```bash
docker-compose up -d
```

4. Acesse:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Documentação da API: http://localhost:8000/docs
- Health check: http://localhost:8000/health

5. Para parar:
```bash
docker-compose down
```

### Desenvolvimento Local

#### Backend
```bash
cd backend

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Configurar .env
cp .env.example .env
# Edite .env com suas credenciais

# Rodar
python main.py
```

#### Frontend
```bash
cd frontend

# Instalar dependências
npm install

# Configurar .env.local
cp .env.local.example .env.local
# Edite .env.local se necessário

# Rodar
npm run dev
```

## 📝 Uso da API

### Autenticação

**Registrar:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "senha123",
    "full_name": "Admin User",
    "organization_name": "Minha Empresa"
  }'
```

**Login:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "senha123"
  }'
```

Resposta:
```json
{
  "access_token": "eyJ0eXAiOiJKV1...",
  "refresh_token": "eyJ0eXAiOiJKV1...",
  "token_type": "bearer"
}
```

### Tickets

**Criar ticket:**
```bash
curl -X POST http://localhost:8000/api/v1/tickets \
  -H "Authorization: Bearer SEU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Problema com login",
    "description": "Não consigo acessar minha conta",
    "priority": "high"
  }'
```

**Listar tickets:**
```bash
curl http://localhost:8000/api/v1/tickets \
  -H "Authorization: Bearer SEU_TOKEN"
```

**Adicionar mensagem:**
```bash
curl -X POST http://localhost:8000/api/v1/tickets/1/messages \
  -H "Authorization: Bearer SEU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Obrigado pelo contato, vou verificar",
    "is_internal": false
  }'
```

### Base de Conhecimento

**Criar artigo:**
```bash
curl -X POST http://localhost:8000/api/v1/knowledge \
  -H "Authorization: Bearer SEU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Como resetar sua senha",
    "slug": "como-resetar-senha",
    "content": "Passo 1: Clique em...",
    "category": "Conta",
    "is_published": true
  }'
```

## 🔒 Segurança

- Senhas hasheadas com bcrypt
- JWT com expiração configurável
- Refresh tokens para renovação segura
- RBAC por organização
- CORS configurável
- Usuários não-root nos containers
- Secrets não commitados (`.env` no `.gitignore`)

## 🧪 Testes

(A implementar)
```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm run test
```

## 📚 Próximos Passos

- [ ] Chatbot com IA
- [ ] Widget embeddable para sites
- [ ] Automações e macros
- [ ] SLA e métricas
- [ ] Webhooks para integrações
- [ ] Email inbound
- [ ] Anexos em tickets
- [ ] Notificações em tempo real (WebSocket)
- [ ] Relatórios e analytics

## 📄 Licença

MIT License

---

Desenvolvido com ❤️ para transformar o atendimento ao cliente.

