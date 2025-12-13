@echo off
echo Iniciando SaaS de Suporte ao Cliente...

docker info >nul 2>&1
if errorlevel 1 (
    echo Docker nao esta rodando. Inicie o Docker e tente novamente.
    exit /b 1
)

echo Construindo e iniciando containers...
docker-compose up -d --build

echo Aguardando servicos ficarem prontos...
timeout /t 10 /nobreak >nul

echo Verificando saude dos servicos...
curl -s http://localhost:8000/health >nul && echo Backend: OK || echo Backend: Falhou
curl -s http://localhost:3000 >nul && echo Frontend: OK || echo Frontend: Falhou

echo.
echo Pronto! Acesse:
echo    Frontend: http://localhost:3000
echo    Backend API: http://localhost:8000
echo    Docs API: http://localhost:8000/docs
echo.
echo Para parar: docker-compose down

