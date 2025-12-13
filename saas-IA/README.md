# SaaS de Suporte ao Cliente

Sistema completo de help desk com chat ao vivo, base de conhecimento e portal de autoatendimento.

## 🚀 Características

### 1. Sistema de Tickets (Help Desk)
- ✅ Criação e gerenciamento de tickets de suporte
- ✅ Atribuição automática e manual de agentes
- ✅ Sistema de prioridades (baixa, média, alta, urgente)
- ✅ Status do ticket (aberto, em progresso, aguardando, resolvido, fechado)
- ✅ Histórico completo de interações
- ✅ Notas internas entre agentes
- ✅ Categorização de tickets

### 2. Chat ao Vivo
- ✅ Atendimento em tempo real
- ✅ Fila de espera para clientes
- ✅ Sistema de aceitação de chats pelos agentes
- ✅ Histórico de conversas
- ✅ Avaliação de atendimento (1-5 estrelas)
- ✅ Feedback dos clientes

### 3. Base de Conhecimento
- ✅ Artigos e tutoriais organizados
- ✅ Sistema de categorias
- ✅ Busca inteligente por texto
- ✅ Tags para melhor organização
- ✅ Contador de visualizações
- ✅ Sistema de avaliação de utilidade
- ✅ Portal de autoatendimento público

### 4. Sistema de Autenticação
- ✅ Registro de usuários
- ✅ Login/Logout seguro
- ✅ Autenticação JWT
- ✅ Três tipos de usuários (Cliente, Agente, Admin)
- ✅ Controle de permissões por role

## 🛠️ Stack Tecnológica

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL 16
- **ORM**: SQLAlchemy 2.0
- **Validação**: Pydantic
- **Autenticação**: JWT (python-jose)
- **Cache**: Redis
- **Migrations**: Alembic

### Frontend
- **Framework**: Next.js 15 (React 18)
- **Linguagem**: TypeScript
- **Styling**: Tailwind CSS
- **Estado**: React Query
- **HTTP Client**: Axios
- **Ícones**: Lucide React

### DevOps
- **Containerização**: Docker & Docker Compose
- **Banco de Dados**: PostgreSQL (containerizado)
- **Cache**: Redis (containerizado)

## 📦 Instalação

### Pré-requisitos
- Docker e Docker Compose instalados
- (Opcional) Python 3.11+ e Node.js 20+ para desenvolvimento local

### Opção 1: Com Docker (Recomendado)

1. Clone o repositório:
```bash
git clone <repository-url>
cd saas
```

2. Inicie os serviços com Docker Compose:
```bash
docker-compose up -d
```

3. Acesse as aplicações:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Documentação da API: http://localhost:8000/api/docs

### Opção 2: Desenvolvimento Local

#### Backend

1. Entre na pasta do backend:
```bash
cd backend
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp env.example .env
# Edite o arquivo .env com suas configurações
```

5. Execute as migrations:
```bash
alembic upgrade head
```

6. Inicie o servidor:
```bash
uvicorn main:app --reload
```

#### Frontend

1. Entre na pasta do frontend:
```bash
cd frontend
```

2. Instale as dependências:
```bash
npm install
```

3. Configure as variáveis de ambiente:
```bash
# Crie um arquivo .env.local
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
```

4. Inicie o servidor de desenvolvimento:
```bash
npm run dev
```

## 📚 Estrutura do Projeto

```
saas/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   ├── auth.py       # Endpoints de autenticação
│   │   │   │   ├── tickets.py    # Endpoints de tickets
│   │   │   │   ├── chats.py      # Endpoints de chat
│   │   │   │   ├── knowledge.py  # Endpoints de base de conhecimento
│   │   │   │   └── router.py     # Router principal
│   │   │   └── deps.py            # Dependências (auth, etc)
│   │   ├── core/
│   │   │   ├── config.py          # Configurações
│   │   │   └── security.py        # Funções de segurança
│   │   ├── db/
│   │   │   └── session.py         # Sessão do banco de dados
│   │   ├── models/
│   │   │   └── models.py          # Modelos SQLAlchemy
│   │   └── schemas/
│   │       └── schemas.py         # Schemas Pydantic
│   ├── main.py                    # Aplicação FastAPI
│   └── requirements.txt           # Dependências Python
├── frontend/
│   ├── app/
│   │   ├── (auth)/
│   │   │   ├── login/             # Página de login
│   │   │   └── register/          # Página de registro
│   │   ├── (dashboard)/
│   │   │   ├── tickets/           # Páginas de tickets
│   │   │   ├── chats/             # Páginas de chat
│   │   │   └── knowledge/         # Páginas de base de conhecimento
│   │   ├── layout.tsx             # Layout principal
│   │   ├── page.tsx               # Página inicial
│   │   └── globals.css            # Estilos globais
│   ├── lib/
│   │   ├── api.ts                 # Cliente da API
│   │   └── types.ts               # Tipos TypeScript
│   ├── components/                # Componentes reutilizáveis
│   ├── package.json               # Dependências Node
│   └── tsconfig.json              # Configuração TypeScript
├── docker/
│   ├── Dockerfile.backend         # Dockerfile do backend
│   └── Dockerfile.frontend        # Dockerfile do frontend
└── docker-compose.yml             # Orquestração de containers

```

## 🔐 Autenticação

O sistema usa JWT (JSON Web Tokens) para autenticação:

1. Usuário faz login com email e senha
2. API retorna um token de acesso
3. Token é armazenado no localStorage do navegador
4. Todas as requisições subsequentes incluem o token no header Authorization

### Tipos de Usuários

- **Cliente**: Pode criar tickets, iniciar chats, ver base de conhecimento
- **Agente**: Todas as permissões de cliente + gerenciar tickets atribuídos, aceitar chats, criar artigos
- **Admin**: Todas as permissões + deletar tickets/artigos, visualizar todos os dados

## 🗄️ Modelos de Dados

### Documentação Arquitetural

Para detalhes completos sobre decisões arquiteturais, diagramas e especificações técnicas, consulte:
- **[📐 Documentação Arquitetural Completa](docs/INDEX.md)** - Índice navegável
- **[ADRs - Architecture Decision Records](docs/adr/)** - Decisões de design
- **[Diagramas C4](docs/architecture/)** - Arquitetura em 3 níveis
- **[Diagramas ER e Índices](docs/diagrams/)** - Modelagem de banco de dados
- **[Diagramas de Fluxo](docs/diagrams/)** - Fluxos de autenticação, tickets, chat

---

### User
- Email, senha, nome completo
- Role (customer, agent, admin)
- Status online/offline

### Ticket
- Título, descrição, categoria
- Status, prioridade
- Cliente e agente atribuído
- Timestamps

### Message
- Conteúdo da mensagem
- Relacionado a ticket ou chat
- Flag de mensagem interna

### ChatSession
- Cliente e agente
- Status (waiting, active, ended)
- Avaliação e feedback

### KnowledgeArticle
- Título, conteúdo, categoria
- Tags, autor
- Contadores de visualizações e utilidade
- Status de publicação

## 🔌 API Endpoints

### Autenticação
- `POST /api/v1/auth/register` - Registrar usuário
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/logout` - Logout

### Tickets
- `GET /api/v1/tickets/` - Listar tickets
- `POST /api/v1/tickets/` - Criar ticket
- `GET /api/v1/tickets/{id}` - Obter ticket
- `PATCH /api/v1/tickets/{id}` - Atualizar ticket
- `DELETE /api/v1/tickets/{id}` - Deletar ticket
- `GET /api/v1/tickets/{id}/messages` - Listar mensagens
- `POST /api/v1/tickets/{id}/messages` - Criar mensagem

### Chat
- `GET /api/v1/chats/` - Listar sessões
- `POST /api/v1/chats/` - Criar sessão
- `GET /api/v1/chats/waiting` - Chats aguardando
- `POST /api/v1/chats/{id}/accept` - Aceitar chat
- `GET /api/v1/chats/{id}/messages` - Listar mensagens
- `POST /api/v1/chats/{id}/messages` - Enviar mensagem

### Base de Conhecimento
- `GET /api/v1/knowledge/` - Listar artigos
- `POST /api/v1/knowledge/` - Criar artigo
- `GET /api/v1/knowledge/{id}` - Obter artigo
- `PATCH /api/v1/knowledge/{id}` - Atualizar artigo
- `DELETE /api/v1/knowledge/{id}` - Deletar artigo
- `POST /api/v1/knowledge/{id}/helpful` - Marcar como útil
- `GET /api/v1/knowledge/categories/list` - Listar categorias

## 🧪 Testando a Aplicação

1. Acesse http://localhost:3000
2. Crie uma conta de teste
3. Explore as funcionalidades:
   - Crie tickets de suporte
   - Inicie conversas no chat
   - Navegue pela base de conhecimento
   - (Como agente) Aceite e responda tickets/chats

## 📝 Variáveis de Ambiente

### Backend (.env)
```env
DATABASE_URL=postgresql://saas_user:saas_password@localhost:5432/saas_support
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=1440
DEBUG=True
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🚀 Deploy em Produção

### Recomendações

1. **Backend**: Railway, Render, AWS ECS
2. **Frontend**: Vercel, Netlify
3. **Database**: PostgreSQL gerenciado (AWS RDS, Railway)
4. **Redis**: Redis gerenciado (Railway, Upstash)

### Checklist de Segurança

- [ ] Alterar SECRET_KEY para valor aleatório forte
- [ ] Configurar CORS adequadamente
- [ ] Usar HTTPS em produção
- [ ] Configurar rate limiting
- [ ] Revisar permissões de usuários
- [ ] Configurar backups do banco de dados
- [ ] Implementar monitoramento e logs

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT.

## 👥 Suporte

Para suporte, abra uma issue no repositório ou entre em contato através do email.

---

**Desenvolvido com ❤️ usando FastAPI e Next.js**

