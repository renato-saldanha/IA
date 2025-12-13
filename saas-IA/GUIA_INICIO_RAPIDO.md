# 🚀 Guia Rápido de Inicialização - SaaS de Suporte ao Cliente

## Início Rápido com Docker (5 minutos)

### 1. Pré-requisitos
- Docker Desktop instalado e rodando
- Git (para clonar o repositório)

### 2. Iniciar o Projeto

```bash
# Entre na pasta do projeto
cd saas

# Inicie todos os serviços
docker-compose up -d

# Aguarde alguns segundos para os serviços iniciarem
# Você pode verificar o status com:
docker-compose ps
```

### 3. Acessar a Aplicação

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentação da API**: http://localhost:8000/api/docs

### 4. Criar Conta de Teste

1. Acesse http://localhost:3000
2. Clique em "Criar Conta"
3. Preencha os dados:
   - Nome: Teste Admin
   - Email: admin@teste.com
   - Tipo: Administrador
   - Senha: teste123456
4. Clique em "Criar Conta"

### 5. Testar Funcionalidades

#### Como Cliente:
1. Crie um ticket de suporte
2. Inicie um chat ao vivo
3. Navegue pela base de conhecimento

#### Como Agente/Admin:
1. Visualize todos os tickets
2. Aceite chats da fila
3. Crie artigos na base de conhecimento

## Comandos Úteis

### Docker Compose

```bash
# Iniciar serviços
docker-compose up -d

# Parar serviços
docker-compose down

# Ver logs
docker-compose logs -f

# Ver logs de um serviço específico
docker-compose logs -f backend
docker-compose logs -f frontend

# Reiniciar um serviço
docker-compose restart backend

# Reconstruir imagens
docker-compose build

# Limpar tudo (incluindo volumes)
docker-compose down -v
```

### Backend

```bash
# Entrar no container do backend
docker-compose exec backend bash

# Criar migrações do banco
docker-compose exec backend alembic revision --autogenerate -m "migration name"

# Aplicar migrações
docker-compose exec backend alembic upgrade head

# Acessar banco de dados
docker-compose exec postgres psql -U saas_user -d saas_support
```

### Frontend

```bash
# Entrar no container do frontend
docker-compose exec frontend sh

# Instalar nova dependência
docker-compose exec frontend npm install <package-name>

# Limpar cache do Next.js
docker-compose exec frontend rm -rf .next
```

## Desenvolvimento Local (Sem Docker)

### Backend

```bash
cd backend

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp env.example .env
# Edite o .env com suas configurações

# Iniciar servidor
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend

# Instalar dependências
npm install

# Configurar variáveis de ambiente
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Iniciar servidor
npm run dev
```

## Estrutura de URLs

### Frontend
- `/` - Página inicial
- `/auth/login` - Login
- `/auth/register` - Registro
- `/dashboard/tickets` - Lista de tickets
- `/dashboard/tickets/new` - Criar ticket
- `/dashboard/tickets/[id]` - Detalhes do ticket
- `/dashboard/chats` - Lista de chats
- `/dashboard/knowledge` - Base de conhecimento

### Backend API
- `/api/v1/auth/*` - Autenticação
- `/api/v1/tickets/*` - Tickets
- `/api/v1/chats/*` - Chat ao vivo
- `/api/v1/knowledge/*` - Base de conhecimento
- `/api/docs` - Documentação Swagger
- `/api/redoc` - Documentação ReDoc

## Troubleshooting

### Problema: Porta já em uso

```bash
# Verificar o que está usando a porta
# Windows
netstat -ano | findstr :3000
netstat -ano | findstr :8000

# Linux/Mac
lsof -i :3000
lsof -i :8000

# Alterar porta no docker-compose.yml
# Mude "3000:3000" para "3001:3000" por exemplo
```

### Problema: Banco de dados não conecta

```bash
# Verificar se o PostgreSQL está rodando
docker-compose ps postgres

# Ver logs do PostgreSQL
docker-compose logs postgres

# Reiniciar PostgreSQL
docker-compose restart postgres
```

### Problema: Frontend não carrega

```bash
# Limpar cache e reinstalar
docker-compose down
docker-compose up --build frontend
```

### Problema: Erro de autenticação

```bash
# Verificar se o SECRET_KEY está configurado
docker-compose exec backend printenv | grep SECRET_KEY

# Limpar tokens no navegador
# Abra DevTools (F12) > Application > Local Storage > Limpar
```

## Dados de Exemplo

### Usuários de Teste

```
Admin:
- Email: admin@teste.com
- Senha: admin123456
- Role: admin

Agente:
- Email: agente@teste.com
- Senha: agente123456
- Role: agent

Cliente:
- Email: cliente@teste.com
- Senha: cliente123456
- Role: customer
```

### Criar Usuários via API

```bash
# Usando curl
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@teste.com",
    "full_name": "Admin Teste",
    "password": "admin123456",
    "role": "admin"
  }'
```

## Próximos Passos

1. ✅ Explore a documentação da API: http://localhost:8000/api/docs
2. ✅ Crie alguns tickets de teste
3. ✅ Experimente o chat ao vivo
4. ✅ Adicione artigos na base de conhecimento
5. ✅ Teste diferentes tipos de usuários (cliente, agente, admin)

## Recursos Adicionais

- 📖 README completo: [README.md](./README.md)
- 🔌 Documentação da API: http://localhost:8000/api/docs
- 📚 Next.js: https://nextjs.org/docs
- 🐍 FastAPI: https://fastapi.tiangolo.com
- 🐳 Docker: https://docs.docker.com

## Precisa de Ajuda?

- Abra uma issue no GitHub
- Verifique os logs: `docker-compose logs -f`
- Consulte a documentação completa no README.md

---

**Boa sorte com seu projeto! 🚀**

