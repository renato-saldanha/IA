# 🪟 Guia de Instalação para Windows

## Pré-requisitos

### 1. Instalar Docker Desktop para Windows

1. Baixe o Docker Desktop: https://www.docker.com/products/docker-desktop/
2. Execute o instalador
3. Reinicie o computador quando solicitado
4. Inicie o Docker Desktop
5. Aguarde o Docker iniciar completamente (ícone na bandeja do sistema)

**Requisitos:**
- Windows 10 64-bit: Pro, Enterprise ou Education (Build 19041 ou superior)
- OU Windows 11 64-bit: Home, Pro, Enterprise ou Education
- WSL 2 habilitado (o instalador faz isso automaticamente)
- Virtualização habilitada na BIOS

### 2. Verificar Instalação

Abra o PowerShell ou CMD e execute:

```powershell
docker --version
docker-compose --version
```

Você deve ver algo como:
```
Docker version 24.0.7, build afdd53b
Docker Compose version v2.23.3-desktop.2
```

## 🚀 Iniciar o Projeto

### Opção 1: Usando o Script (Mais Fácil)

1. Abra o Explorador de Arquivos
2. Navegue até a pasta `saas`
3. Clique duas vezes em `start.bat`
4. Aguarde a inicialização (aparecerá uma janela do terminal)

### Opção 2: Linha de Comando

1. Abra o PowerShell ou CMD
2. Navegue até a pasta do projeto:

```powershell
cd F:\MCP\create_fullstack_products\saas
```

3. Execute:

```powershell
docker-compose up -d
```

## 🌐 Acessar a Aplicação

Após alguns segundos, acesse:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentação**: http://localhost:8000/api/docs

## 🛑 Parar o Projeto

### Usando o Script

Crie um arquivo `stop.bat` na pasta `saas` com:

```batch
@echo off
echo Parando servicos...
docker-compose down
echo Servicos parados!
pause
```

Ou execute no terminal:

```powershell
docker-compose down
```

## 🔧 Solução de Problemas

### Problema: "Docker não está instalado"

**Solução:**
1. Verifique se o Docker Desktop está instalado
2. Inicie o Docker Desktop manualmente
3. Aguarde aparecer "Docker Desktop is running" na bandeja

### Problema: "WSL 2 installation is incomplete"

**Solução:**
1. Abra PowerShell como Administrador
2. Execute:

```powershell
wsl --install
```

3. Reinicie o computador
4. Inicie o Docker Desktop novamente

### Problema: Porta 3000 ou 8000 já está em uso

**Solução 1 - Descobrir o que está usando a porta:**

```powershell
netstat -ano | findstr :3000
netstat -ano | findstr :8000
```

Anote o PID (último número) e finalize o processo:

```powershell
taskkill /PID <numero_do_pid> /F
```

**Solução 2 - Mudar a porta no docker-compose.yml:**

Edite o arquivo `docker-compose.yml` e mude:
- `"3000:3000"` para `"3001:3000"` (frontend)
- `"8000:8000"` para `"8001:8000"` (backend)

### Problema: Erro "permission denied" ou "access denied"

**Solução:**
1. Execute o PowerShell como Administrador
2. Navegue até a pasta do projeto
3. Execute os comandos Docker

### Problema: Containers não iniciam

**Solução:**
1. Veja os logs:

```powershell
docker-compose logs
```

2. Reinicie todos os containers:

```powershell
docker-compose restart
```

3. Se o problema persistir, reconstrua:

```powershell
docker-compose down -v
docker-compose up --build -d
```

### Problema: Frontend mostra erro de conexão

**Solução:**
1. Verifique se o backend está rodando:

```powershell
docker-compose ps
```

2. Teste o backend diretamente:

```powershell
curl http://localhost:8000/health
```

Ou abra http://localhost:8000/health no navegador.

### Problema: Banco de dados não conecta

**Solução:**
1. Verifique os logs do PostgreSQL:

```powershell
docker-compose logs postgres
```

2. Reinicie o PostgreSQL:

```powershell
docker-compose restart postgres
```

3. Se necessário, limpe os volumes:

```powershell
docker-compose down -v
docker-compose up -d
```

## 📊 Comandos Úteis do Docker no Windows

### Ver containers rodando
```powershell
docker ps
```

### Ver todos os containers
```powershell
docker ps -a
```

### Ver logs de um container específico
```powershell
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

### Entrar em um container
```powershell
docker-compose exec backend bash
docker-compose exec frontend sh
```

### Verificar uso de recursos
```powershell
docker stats
```

### Limpar sistema Docker
```powershell
# Remover containers parados
docker container prune

# Remover imagens não usadas
docker image prune

# Limpar tudo (cuidado!)
docker system prune -a
```

## 🔄 Atualizar o Projeto

Se você fez mudanças no código:

```powershell
# Parar containers
docker-compose down

# Reconstruir imagens
docker-compose build

# Iniciar novamente
docker-compose up -d
```

## 📝 Desenvolvimento Local (Sem Docker)

Se preferir rodar sem Docker:

### Backend

1. Instale Python 3.11: https://www.python.org/downloads/
2. Abra PowerShell na pasta `backend`:

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

3. Configure o `.env`:

```powershell
copy env.example .env
notepad .env
```

4. Inicie o servidor:

```powershell
uvicorn main:app --reload
```

### Frontend

1. Instale Node.js 20: https://nodejs.org/
2. Abra PowerShell na pasta `frontend`:

```powershell
cd frontend
npm install
```

3. Configure o `.env.local`:

```powershell
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
```

4. Inicie o servidor:

```powershell
npm run dev
```

## 🎯 Dicas Importantes

- ✅ Sempre inicie o Docker Desktop antes de usar os comandos
- ✅ Use PowerShell ou CMD, não o Git Bash para comandos Docker
- ✅ Execute como Administrador se tiver problemas de permissão
- ✅ Aguarde os serviços iniciarem completamente (10-15 segundos)
- ✅ Verifique o Firewall do Windows se não conseguir acessar as URLs

## 🆘 Ainda com Problemas?

1. Reinicie o Docker Desktop
2. Reinicie o computador
3. Verifique se a virtualização está habilitada na BIOS
4. Consulte os logs: `docker-compose logs -f`
5. Reinstale o Docker Desktop se necessário

## 📚 Recursos Adicionais

- Docker Desktop Docs: https://docs.docker.com/desktop/windows/
- WSL 2 Setup: https://docs.microsoft.com/en-us/windows/wsl/install
- Docker Troubleshooting: https://docs.docker.com/desktop/troubleshoot/overview/

---

**Boa sorte com seu projeto no Windows! 🪟🚀**

