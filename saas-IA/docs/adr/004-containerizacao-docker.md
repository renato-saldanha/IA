# ADR 004: Containerização com Docker Compose

## Status
**Aceito** - 2024-12-07

## Decisores
- DevOps Engineer
- Tech Lead
- Backend Developer
- Frontend Developer

## Contexto

O projeto SaaS de Suporte ao Cliente envolve múltiplos serviços (frontend, backend, PostgreSQL, Redis) que precisam rodar juntos em desenvolvimento e produção. Precisamos de uma solução que:

- Facilite setup do ambiente de desenvolvimento
- Garanta consistência entre desenvolvimento e produção
- Permita fácil onboarding de novos desenvolvedores
- Suporte para Windows, macOS e Linux
- Isole dependências e versões
- Facilite deploy em cloud providers

### Alternativas Consideradas:
1. **Docker Compose** - Orquestração multi-container
2. **Kubernetes** - Orquestração enterprise-grade
3. **VM-based** - Vagrant ou virtualização tradicional
4. **Native setup** - Instalação manual em cada máquina

## Decisão

Escolhemos **Docker Compose** para desenvolvimento e deploy inicial.

### Justificativa:

**Vantagens do Docker Compose:**
- **Simplicidade**: Um comando para subir toda stack (`docker-compose up`)
- **Declarativo**: Arquivo YAML descreve toda infraestrutura
- **Isolamento**: Cada serviço em container separado
- **Portabilidade**: Funciona igual em qualquer SO
- **Reprodutibilidade**: Ambientes idênticos para todos desenvolvedores
- **Network automático**: Containers se comunicam por nome
- **Volumes**: Persistência de dados fácil
- **Hot reload**: Code changes refletem sem rebuild (em dev)
- **Resource control**: Limites de CPU/memória por serviço

**Por que não Kubernetes:**
- Overhead desnecessário para projeto inicial
- Complexidade de configuração muito maior
- Curva de aprendizado íngreme
- Recursos necessários (CPU/RAM) muito maiores
- Podemos migrar para K8s futuramente se necessário

**Por que não VM-based:**
- Muito mais pesado que containers
- Setup mais lento
- Consome mais recursos
- Docker é o padrão da indústria atualmente

**Por que não Native setup:**
- Inconsistências entre máquinas
- Conflitos de versões (Python, Node, PostgreSQL)
- Onboarding difícil (horas de setup)
- Difícil garantir paridade dev/prod

## Consequências

### Positivas:
- ✅ **Onboarding rápido**: Novo dev pronto em 5 minutos
- ✅ **Consistência**: "Funciona na minha máquina" deixa de existir
- ✅ **Isolamento**: Não interfere com outros projetos no host
- ✅ **CI/CD ready**: Mesmas imagens usadas em dev, staging e prod
- ✅ **Cleanup fácil**: `docker-compose down -v` limpa tudo
- ✅ **Multi-plataforma**: Windows, macOS, Linux
- ✅ **Debugging**: Logs centralizados (`docker-compose logs`)
- ✅ **Escalabilidade**: Fácil adicionar novos serviços

### Negativas:
- ⚠️ **Docker Desktop required**: Desenvolvedores precisam instalar Docker
- ⚠️ **Recursos**: Containers consomem CPU/RAM
- ⚠️ **Windows WSL2**: Requer configuração no Windows
- ⚠️ **Learning curve**: Devs precisam entender Docker básico
- ⚠️ **Build time**: Primeira build pode demorar

### Riscos Mitigados:
- Scripts de setup automático (start.sh, start.bat)
- Documentação detalhada (WINDOWS_SETUP.md)
- Health checks nos containers
- Volumes nomeados para persistência
- Network isolado para segurança

## Arquitetura Docker Compose

### Serviços:

```yaml
services:
  frontend:    # Next.js (port 3000)
  backend:     # FastAPI (port 8000)
  postgres:    # PostgreSQL 16 (port 5432)
  redis:       # Redis 7 (port 6379)
```

### Network:
- Todos containers na mesma rede Docker
- Comunicação por nome do serviço
- Frontend → `http://backend:8000`
- Backend → `postgres:5432`, `redis:6379`

### Volumes:
- `postgres_data`: Dados PostgreSQL persistentes
- `redis_data`: Dados Redis persistentes
- Bind mounts para hot reload (dev)

### Health Checks:
- PostgreSQL: `pg_isready -U saas_user`
- Redis: `redis-cli ping`
- Backend: Aguarda PostgreSQL e Redis
- Frontend: Aguarda Backend

## Configuração

### docker-compose.yml principal:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: saas_user
      POSTGRES_PASSWORD: saas_password
      POSTGRES_DB: saas_support
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U saas_user"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]

  backend:
    build: ./backend
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    environment:
      DATABASE_URL: postgresql://saas_user:saas_password@postgres:5432/saas_support
      REDIS_URL: redis://redis:6379/0
    volumes:
      - ./backend:/app  # Hot reload

  frontend:
    build: ./frontend
    depends_on:
      - backend
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8000
    volumes:
      - ./frontend:/app  # Hot reload
      - /app/node_modules  # Evitar override

volumes:
  postgres_data:
  redis_data:
```

### Dockerfiles:

**Backend (Multi-stage):**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

**Frontend:**
```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
CMD ["npm", "run", "dev"]
```

## Comandos Principais

```bash
# Iniciar tudo
docker-compose up -d

# Ver logs
docker-compose logs -f
docker-compose logs -f backend

# Parar tudo
docker-compose down

# Parar e limpar volumes
docker-compose down -v

# Reconstruir imagens
docker-compose build

# Reiniciar um serviço
docker-compose restart backend

# Executar comando em container
docker-compose exec backend bash
docker-compose exec postgres psql -U saas_user
```

## Alternativas Consideradas

| Solução | Prós | Contras | Decisão |
|---------|------|---------|---------|
| Docker Compose | Simples, declarativo, padrão | Não escala enterprise | ✅ Escolhido |
| Kubernetes | Escala, resiliente, produção | Complexo, overhead | ❌ Rejeitado (por ora) |
| VMs | Isolamento total | Pesado, lento | ❌ Rejeitado |
| Native | Sem overhead | Inconsistente, difícil | ❌ Rejeitado |

## Deploy em Produção

Para produção, planejamos usar:
- **Frontend**: Vercel (otimizado para Next.js)
- **Backend**: Railway ou Render (com Docker)
- **PostgreSQL**: Managed service (Railway/AWS RDS)
- **Redis**: Managed service (Railway/Upstash)

Futuro: Migração para Kubernetes se necessário (100k+ usuários).

## Referências
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Multi-stage builds](https://docs.docker.com/build/building/multi-stage/)

## Notas de Implementação
- Docker Compose versão: 3.8
- Imagens base: Alpine Linux (menores)
- Health checks em todos serviços críticos
- Volumes nomeados para dados persistentes
- Bind mounts para hot reload em desenvolvimento
- Scripts de inicialização: start.sh (Linux/Mac), start.bat (Windows)

