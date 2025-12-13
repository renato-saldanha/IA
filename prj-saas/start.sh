#!/bin/bash

echo "🚀 Iniciando SaaS de Suporte ao Cliente..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker não está rodando. Inicie o Docker e tente novamente."
    exit 1
fi

# Build and start containers
echo "📦 Construindo e iniciando containers..."
docker-compose up -d --build

# Wait for services to be ready
echo "⏳ Aguardando serviços ficarem prontos..."
sleep 10

# Check health
echo "🏥 Verificando saúde dos serviços..."
curl -s http://localhost:8000/health > /dev/null && echo "✅ Backend: OK" || echo "❌ Backend: Falhou"
curl -s http://localhost:3000 > /dev/null && echo "✅ Frontend: OK" || echo "❌ Frontend: Falhou"

echo ""
echo "✨ Pronto! Acesse:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   Docs API: http://localhost:8000/docs"
echo ""
echo "Para parar: docker-compose down"

