# Sistema de Gerenciamento de Cemitérios e Jazigos do Governo

Sistema completo de gerenciamento de cemitérios e jazigos com interface moderna, controle de permissões por setor, sistema de logs e exclusão lógica.

## 🚀 Tecnologias

### Backend
- **Python** com FastAPI
- **PostgreSQL** - Banco de dados principal
- **Redis** - Cache e sessões
- **JWT** - Autenticação e autorização

### Frontend
- **Next.js 16** - Framework React
- **Tailwind CSS** - Estilização
- **shadcn/ui** - Componentes UI
- **NextAuth.js** - Autenticação

### Testes
- **Playwright** - Testes E2E
- **Vitest** - Testes unitários frontend
- **Jest** - Testes backend

### Documentação
- **OpenAPI/Swagger** - Documentação da API
- **Storybook** - Documentação de componentes

## 📋 Funcionalidades

- ✅ Tela de login visualmente atrativa e simplista
- ✅ Dashboard com menu lateral
- ✅ Sistema de abas superior para múltiplos menus abertos
- ✅ Cadastros e consultas de cemitérios e jazigos
- ✅ Relatórios e gráficos com métricas
- ✅ Configurações e parametrização de permissões por setor
- ✅ Sistema de logs para todas as operações
- ✅ Exclusão lógica de registros

## 🏗️ Estrutura do Projeto

```
cemiterio_governo/
├── backend/          # API FastAPI
├── frontend/         # Aplicação Next.js
├── docs/            # Documentação
└── docker-compose.yml
```

## 🚀 Início Rápido

### Pré-requisitos
- Docker e Docker Compose
- Node.js 20+
- Python 3.12+

### Executar com Docker

```bash
docker-compose up -d
```

### Executar localmente

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 📚 Documentação

- API: http://localhost:8000/docs
- Storybook: http://localhost:6006
- Frontend: http://localhost:3000

## 🔐 Autenticação

O sistema utiliza NextAuth.js no frontend e JWT no backend para autenticação segura.

## 📝 Logs

Todas as operações de inserção e alteração são registradas automaticamente no sistema de logs.

## 🗑️ Exclusão Lógica

Todos os registros são excluídos logicamente (soft delete), mantendo o histórico completo.
