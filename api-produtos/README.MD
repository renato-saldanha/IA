# API de Produtos (Node.js + Express)

Descrição
- API RESTful para gerenciamento de produtos.
- Arquitetura: Repository Pattern + Service Layer.
- Validações de entrada com express-validator.
- Persistência simples em arquivo JSON (data/products.json).
- Ideal para testes locais com Insomnia; concebida para evolução para banco real.

Requisitos
- Node.js v16+ (testado em v24)
- npm
- Windows (comandos do guia em PowerShell/CMD)

Instalação (Windows)
1. Abra o terminal do VS Code ou PowerShell.
2. Navegue até a pasta do projeto:
   cd /d f:\Projetos\IA\api-node
3. Instale dependências:
   npm install

Scripts úteis (package.json)
- npm run start  -> inicia produção (node src/index.js)
- npm run dev    -> inicia com nodemon (monitoramento durante desenvolvimento)

Variáveis de ambiente
- PORT (opcional) — porta do servidor (padrão: 3000)

Estrutura principal
- src/
  - index.js         -> inicializa servidor
  - app.js           -> configura express, rotas e middleware de erro
  - routes/          -> rotas (productsRoutes.js)
  - controllers/     -> controllers (productController.js)
  - services/        -> regras de negócio (productService.js)
  - repositories/    -> acesso a dados (productRepository.js)
  - scripts/         -> scripts utilitários (testRepository.js) — opcional
- data/
  - products.json    -> armazenamento local (JSON)

Primeira execução
1. Assegure que data/products.json existe e contém: []
2. Inicie servidor:
   npm run start
3. Verifique rota raiz:
   http://localhost:3000/
   -> Resposta: "API de produtos rodando!"

Testes com Insomnia (exemplos)
- Base URL: http://localhost:3000/products

1) Criar produto (POST /products)
URL: http://localhost:3000/products
Body (JSON):
{
  "name": "Camiseta",
  "price": 49.9,
  "stock": 10,
  "description": "Camiseta 100% algodão"
}
Resposta esperada: 201 Created (objeto com id)

2) Listar produtos (GET /products)
URL: http://localhost:3000/products
Resposta: 200 OK (array de produtos)

3) Obter por id (GET /products/:id)
URL: http://localhost:3000/products/{id}
Resposta: 200 OK ou 404 se não encontrado

4) Atualizar produto (PUT /products/:id)
URL: http://localhost:3000/products/{id}
Body (JSON) — validações aplicadas (name mínimo 3 chars, price > 0):
{
  "name": "Camiseta Nova",
  "price": 59.9,
  "stock": 8,
  "description": "Atualizada"
}
Resposta: 200 OK ou 400/404 conforme validação/negócio

5) Remover produto (DELETE /products/:id)
URL: http://localhost:3000/products/{id}
Resposta: 204 No Content ou 404 se não encontrado

Validações implementadas
- name: obrigatório, string, mínimo 3 caracteres
- price: obrigatório, número > 0
- stock: opcional, inteiro >= 0
- description: opcional, string
- Regras de negócio: não permite nomes duplicados (case-insensitive)

Scripts de teste local (opcional)
- node src\scripts\testRepository.js  -> executa testes rápidos do repositório (criar/listar/buscar)

Boas práticas e próximos passos
- Substituir data/products.json por banco relacional/NoSQL (Postgres, MySQL, MongoDB).
- Adicionar migrations e ORM ou query builder (TypeORM, Sequelize, Prisma, Knex).
- Implementar autenticação (JWT), rate-limiting e CORS.
- Adicionar testes automatizados (Jest/Supertest) e CI/CD.

Problemas comuns
- Erro "argument handler must be a function": verifique se o arquivo de rotas está exportando um Router (module.exports = router).
- Permissões de escrita em data/products.json: garantir permissões no Windows.


Prompt usado:


"""

Me ensine como criar uma API RESTful em NodeJS(Express) para gerenciar produtos. Inclua validações de entrada nos endpoints de criação e edição. Use o padrão de projeto Repository Pattern+Service Layer. Gere os códigos com comentários explicativos(em portguês do Brasil). Usaremos Insomnia para testes da API(Inserção, edição, etc). Crie um passo a passo do inicio ao fim da criação da API.

Valide cada etapa antes de ir para a próxima.
Gere o passo a passo de cada etapa de como fazer.


"""