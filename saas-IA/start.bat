@echo off
REM Script de inicialização para Windows

echo ========================================
echo   SaaS de Suporte ao Cliente
echo ========================================
echo.

REM Verificar se Docker está instalado
docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Docker não está instalado!
    echo Por favor, instale o Docker Desktop: https://docs.docker.com/desktop/install/windows-install/
    pause
    exit /b 1
)

REM Verificar se Docker está rodando
docker info >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Docker não está rodando!
    echo Por favor, inicie o Docker Desktop
    pause
    exit /b 1
)

echo [OK] Docker encontrado e rodando
echo.

REM Iniciar serviços
echo Iniciando containers...
docker-compose up -d

echo.
echo Aguardando servicos iniciarem...
timeout /t 10 /nobreak >nul

REM Verificar status
echo.
echo Status dos servicos:
docker-compose ps

echo.
echo ========================================
echo   Aplicacao iniciada com sucesso!
echo ========================================
echo.
echo Acesse:
echo   Frontend: http://localhost:3000
echo   Backend API: http://localhost:8000
echo   Documentacao: http://localhost:8000/api/docs
echo.
echo Para ver os logs:
echo   docker-compose logs -f
echo.
echo Para parar:
echo   docker-compose down
echo.
pause

