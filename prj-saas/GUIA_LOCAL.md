# Guia de Execução Local (Sem Docker)

## Pré-requisitos
- Python 3.11+
- Node.js 20+
- PostgreSQL 16
- Redis 7

## 1. Configurar Banco de Dados

### PostgreSQL
```powershell
# Crie o banco de dados
psql -U postgres
CREATE DATABASE support_saas;
CREATE USER support_user WITH PASSWORD 'support_pass';
GRANT ALL PRIVILEGES ON DATABASE support_saas TO support_user;
\q
```

### Redis
Instale e inicie o Redis ou use uma instância na nuvem.

## 2. Backend (FastAPI)

```powershell
cd backend

# Criar ambiente virtual
python -m venv venv
.\venv\Scripts\Activate.ps1

# Instalar dependências
pip install -r requirements.txt

# Configurar .env
Copy-Item .env.example .env
# Edite .env com suas credenciais:
# DATABASE_URL=postgresql://support_user:support_pass@localhost:5432/support_saas
# REDIS_URL=redis://localhost:6379/0
# SECRET_KEY=gere-uma-chave-secreta-forte-aqui

# Rodar servidor
python main.py
```

Backend estará em: http://localhost:8000

## 3. Frontend (Next.js)

```powershell
cd frontend

# Instalar dependências
npm install --legacy-peer-deps

# Configurar .env.local
Copy-Item .env.local.example .env.local
# Edite se necessário:
# NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

# Rodar desenvolvimento
npm run dev
```

Frontend estará em: http://localhost:3000

## 4. Testar

### Registrar usuário
```powershell
curl -X POST http://localhost:8000/api/v1/auth/register `
  -H "Content-Type: application/json" `
  -d '{
    "email": "admin@example.com",
    "password": "senha123",
    "full_name": "Admin User",
    "organization_name": "Minha Empresa"
  }'
```

### Login
```powershell
curl -X POST http://localhost:8000/api/v1/auth/login `
  -H "Content-Type: application/json" `
  -d '{
    "email": "admin@example.com",
    "password": "senha123"
  }'
```

## Solução de Problemas

### Postgres Connection Error
- Verifique se o PostgreSQL está rodando
- Confirme credenciais no `.env`
- Teste conexão: `psql -U support_user -d support_saas`

### Redis Connection Error
- Verifique se o Redis está rodando
- Teste: `redis-cli ping` (deve retornar PONG)

### Frontend não conecta ao Backend
- Confirme que backend está em `http://localhost:8000`
- Verifique CORS no `app/core/config.py`
- Verifique `NEXT_PUBLIC_API_URL` no `.env.local`

## Docker (Quando funcionar)

```powershell
# Reinicie o Docker Desktop
Stop-Process -Name "Docker Desktop" -Force
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"

# Aguarde 30-60s, então:
docker-compose up -d --build
```

