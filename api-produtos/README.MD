# 📦 API de Produtos

API RESTful para gerenciamento de produtos desenvolvida em Node.js com Express, seguindo padrões de arquitetura limpa e boas práticas de desenvolvimento.

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Arquitetura](#arquitetura)
- [Tecnologias](#tecnologias)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Documentação da API](#documentação-da-api)
- [Modelo de Dados](#modelo-de-dados)
- [Validações](#validações)
- [Tratamento de Erros](#tratamento-de-erros)
- [Exemplos de Uso](#exemplos-de-uso)
- [Desenvolvimento](#desenvolvimento)
- [Próximos Passos](#próximos-passos)

---

## 🎯 Visão Geral

Esta API fornece endpoints RESTful completos para operações CRUD (Create, Read, Update, Delete) de produtos. O projeto foi desenvolvido seguindo o padrão **Repository Pattern + Service Layer**, garantindo separação de responsabilidades, manutenibilidade e testabilidade.

### Características Principais

- ✅ Arquitetura em camadas (Repository, Service, Controller)
- ✅ Validação de dados de entrada com `express-validator`
- ✅ Persistência de dados em arquivo JSON (pronto para migração para banco de dados)
- ✅ Tratamento centralizado de erros
- ✅ Código documentado e organizado
- ✅ Geração automática de IDs únicos (UUID v4)

---

## 🏗️ Arquitetura

O projeto segue uma arquitetura em camadas que separa as responsabilidades:

```
┌─────────────────────────────────────┐
│         Routes Layer                │  ← Define rotas e validações
├─────────────────────────────────────┤
│       Controller Layer              │  ← Processa requisições/respostas
├─────────────────────────────────────┤
│        Service Layer                │  ← Lógica de negócio
├─────────────────────────────────────┤
│      Repository Layer               │  ← Acesso a dados
├─────────────────────────────────────┤
│         Data Layer                  │  ← Persistência (JSON)
└─────────────────────────────────────┘
```

### Camadas

1. **Routes**: Define as rotas HTTP e aplica validações de entrada
2. **Controller**: Recebe requisições, valida dados e formata respostas
3. **Service**: Contém a lógica de negócio (regras, validações de negócio)
4. **Repository**: Abstrai o acesso aos dados (leitura/escrita)
5. **Data**: Camada de persistência (atualmente arquivo JSON)

---

## 🛠️ Tecnologias

### Dependências Principais

- **Node.js** v16+ (testado em v24)
- **Express** ^5.1.0 - Framework web para Node.js
- **express-validator** ^7.3.1 - Validação de dados de entrada
- **uuid** ^13.0.0 - Geração de identificadores únicos

### Dependências de Desenvolvimento

- **nodemon** ^3.1.11 - Monitoramento automático de alterações durante desenvolvimento

---

## 📁 Estrutura do Projeto

```
api-produtos/
├── src/
│   ├── index.js                    # Ponto de entrada da aplicação
│   ├── app.js                      # Configuração do Express e middlewares
│   ├── routes/
│   │   └── productsRoutes.js       # Rotas de produtos
│   ├── controllers/
│   │   └── productController.js    # Controllers de produtos
│   ├── services/
│   │   └── productService.js       # Lógica de negócio
│   ├── repositories/
│   │   └── productRepository.js    # Acesso a dados
│   └── scripts/
│       └── testRepository.js       # Scripts de teste (opcional)
├── data/
│   └── products.json               # Armazenamento de dados (JSON)
├── package.json                    # Dependências e scripts
└── README.md                       # Documentação
```

---

## 🚀 Instalação

### Pré-requisitos

- Node.js v16 ou superior
- npm (geralmente incluído com Node.js)
- Git (opcional, para clonar o repositório)

### Passos de Instalação

1. **Clone o repositório** (ou navegue até a pasta do projeto):
 
2. **Instale as dependências**:
   ```bash
   npm install
   ```

3. **Verifique se o arquivo de dados existe**:
   - Certifique-se de que `data/products.json` existe
   - Se não existir, crie o arquivo com conteúdo: `[]`

4. **Inicie o servidor**:
   ```bash
   npm start
   # ou para desenvolvimento com auto-reload:
   npm run dev
   ```

5. **Verifique se está funcionando**:
   - Acesse: `http://localhost:3000/`
   - Você deve ver: `"API de produtos rodando!"`

---

## ⚙️ Configuração

### Variáveis de Ambiente

O projeto suporta as seguintes variáveis de ambiente:

| Variável | Descrição | Padrão | Obrigatório |
|----------|-----------|--------|-------------|
| `PORT` | Porta em que o servidor irá rodar | `3000` | Não |

### Exemplo de Configuração

Crie um arquivo `.env` na raiz do projeto (opcional):

```env
PORT=3000
```

---

## 📚 Documentação da API

### Base URL

```
http://localhost:3000
```

### Endpoints

#### 1. Listar Todos os Produtos

Retorna uma lista com todos os produtos cadastrados.

**Endpoint:** `GET /products`

**Resposta de Sucesso (200 OK):**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Camiseta",
    "price": 49.9,
    "stock": 10,
    "description": "Camiseta 100% algodão"
  },
  {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "name": "Calça Jeans",
    "price": 129.9,
    "stock": 5,
    "description": "Calça jeans masculina"
  }
]
```

---

#### 2. Obter Produto por ID

Retorna os detalhes de um produto específico.

**Endpoint:** `GET /products/:id`

**Parâmetros de URL:**
- `id` (string, obrigatório) - ID único do produto (UUID)

**Resposta de Sucesso (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Camiseta",
  "price": 49.9,
  "stock": 10,
  "description": "Camiseta 100% algodão"
}
```

**Resposta de Erro (404 Not Found):**
```json
{
  "message": "Produto não encontrado"
}
```

---

#### 3. Criar Novo Produto

Cria um novo produto no sistema.

**Endpoint:** `POST /products`

**Body (JSON):**
```json
{
  "name": "Camiseta",
  "price": 49.9,
  "stock": 10,
  "description": "Camiseta 100% algodão"
}
```

**Resposta de Sucesso (201 Created):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Camiseta",
  "price": 49.9,
  "stock": 10,
  "description": "Camiseta 100% algodão"
}
```

**Resposta de Erro (400 Bad Request):**
```json
{
  "message": "Dados inválidos",
  "details": [
    {
      "msg": "name deve ter pelo menos 3 caracteres",
      "param": "name",
      "location": "body"
    }
  ]
}
```

**Resposta de Erro - Nome Duplicado (400 Bad Request):**
```json
{
  "message": "Já existe um produto com esse nome"
}
```

---

#### 4. Atualizar Produto

Atualiza os dados de um produto existente.

**Endpoint:** `PUT /products/:id`

**Parâmetros de URL:**
- `id` (string, obrigatório) - ID único do produto (UUID)

**Body (JSON):**
```json
{
  "name": "Camiseta Nova",
  "price": 59.9,
  "stock": 8,
  "description": "Camiseta atualizada"
}
```

**Resposta de Sucesso (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Camiseta Nova",
  "price": 59.9,
  "stock": 8,
  "description": "Camiseta atualizada"
}
```

**Resposta de Erro (404 Not Found):**
```json
{
  "message": "Produto não encontrado"
}
```

**Resposta de Erro - Nome Duplicado (400 Bad Request):**
```json
{
  "message": "Outro produto já usa esse nome"
}
```

---

#### 5. Remover Produto

Remove um produto do sistema.

**Endpoint:** `DELETE /products/:id`

**Parâmetros de URL:**
- `id` (string, obrigatório) - ID único do produto (UUID)

**Resposta de Sucesso (204 No Content):**
```
(sem conteúdo)
```

**Resposta de Erro (404 Not Found):**
```json
{
  "message": "Produto não encontrado"
}
```

---

## 📊 Modelo de Dados

### Produto (Product)

| Campo | Tipo | Obrigatório | Descrição | Validações |
|-------|------|-------------|-----------|------------|
| `id` | string (UUID) | Auto-gerado | Identificador único do produto | Gerado automaticamente |
| `name` | string | Sim | Nome do produto | Mínimo 3 caracteres |
| `price` | number (float) | Sim | Preço do produto | Deve ser maior que 0 |
| `stock` | number (integer) | Não | Quantidade em estoque | Deve ser >= 0 (padrão: 0) |
| `description` | string | Não | Descrição do produto | Texto livre |

### Exemplo de Objeto Produto

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Camiseta Básica",
  "price": 49.9,
  "stock": 10,
  "description": "Camiseta 100% algodão, cores variadas"
}
```

---

## ✅ Validações

### Validações de Entrada (express-validator)

#### Campo `name`
- ✅ Obrigatório
- ✅ Deve ser uma string
- ✅ Mínimo de 3 caracteres

#### Campo `price`
- ✅ Obrigatório
- ✅ Deve ser um número (float)
- ✅ Deve ser maior que 0

#### Campo `stock`
- ⚠️ Opcional
- ✅ Se fornecido, deve ser um número inteiro
- ✅ Deve ser >= 0

#### Campo `description`
- ⚠️ Opcional
- ✅ Se fornecido, deve ser uma string

### Regras de Negócio

1. **Nome Único**: Não é permitido criar produtos com nomes duplicados (case-insensitive)
2. **Atualização de Nome**: Ao atualizar, não é permitido usar um nome que já existe em outro produto

---

## ⚠️ Tratamento de Erros

A API utiliza um middleware centralizado de tratamento de erros que retorna respostas padronizadas.

### Códigos de Status HTTP

| Código | Descrição | Quando Ocorre |
|--------|-----------|---------------|
| 200 | OK | Operação bem-sucedida (GET, PUT) |
| 201 | Created | Produto criado com sucesso |
| 204 | No Content | Produto removido com sucesso |
| 400 | Bad Request | Dados inválidos ou regra de negócio violada |
| 404 | Not Found | Recurso não encontrado |
| 500 | Internal Server Error | Erro interno do servidor |

### Formato de Resposta de Erro

```json
{
  "message": "Mensagem de erro descritiva",
  "details": [
    {
      "msg": "Detalhe específico do erro",
      "param": "campo",
      "location": "body"
    }
  ]
}
```

### Exemplos de Erros

**Validação Falhou:**
```json
{
  "message": "Dados inválidos",
  "details": [
    {
      "msg": "name deve ter pelo menos 3 caracteres",
      "param": "name",
      "location": "body"
    },
    {
      "msg": "price deve ser número maior que 0",
      "param": "price",
      "location": "body"
    }
  ]
}
```

**Produto Não Encontrado:**
```json
{
  "message": "Produto não encontrado"
}
```

**Nome Duplicado:**
```json
{
  "message": "Já existe um produto com esse nome"
}
```

---

## 💡 Exemplos de Uso

### Usando cURL

#### Listar todos os produtos
```bash
curl -X GET http://localhost:3000/products
```

#### Obter produto por ID
```bash
curl -X GET http://localhost:3000/products/550e8400-e29b-41d4-a716-446655440000
```

#### Criar novo produto
```bash
curl -X POST http://localhost:3000/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Camiseta",
    "price": 49.9,
    "stock": 10,
    "description": "Camiseta 100% algodão"
  }'
```

#### Atualizar produto
```bash
curl -X PUT http://localhost:3000/products/550e8400-e29b-41d4-a716-446655440000 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Camiseta Nova",
    "price": 59.9,
    "stock": 8,
    "description": "Camiseta atualizada"
  }'
```

#### Remover produto
```bash
curl -X DELETE http://localhost:3000/products/550e8400-e29b-41d4-a716-446655440000
```

### Usando Insomnia/Postman

1. **Base URL**: `http://localhost:3000`
2. **Headers**: `Content-Type: application/json` (para POST e PUT)
3. **Body**: Use formato JSON para requisições POST e PUT

### Exemplo Completo de Fluxo

```bash
# 1. Criar um produto
POST http://localhost:3000/products
{
  "name": "Notebook",
  "price": 2999.99,
  "stock": 5,
  "description": "Notebook Dell Inspiron 15"
}

# Resposta: 201 Created com o produto criado (incluindo ID)

# 2. Listar todos os produtos
GET http://localhost:3000/products

# 3. Obter o produto criado
GET http://localhost:3000/products/{id-retornado}

# 4. Atualizar o produto
PUT http://localhost:3000/products/{id-retornado}
{
  "name": "Notebook Dell",
  "price": 2799.99,
  "stock": 3,
  "description": "Notebook Dell Inspiron 15 - Promoção"
}

# 5. Remover o produto
DELETE http://localhost:3000/products/{id-retornado}
```

---

## 🔧 Desenvolvimento

### Scripts Disponíveis

| Comando | Descrição |
|---------|-----------|
| `npm start` | Inicia o servidor em modo produção |
| `npm run dev` | Inicia o servidor em modo desenvolvimento com auto-reload (nodemon) |

### Estrutura de Código

O código está organizado seguindo o padrão Repository + Service Layer:

- **Repository**: Abstrai o acesso aos dados, permitindo fácil migração para banco de dados
- **Service**: Contém toda a lógica de negócio e validações específicas
- **Controller**: Processa requisições HTTP e formata respostas
- **Routes**: Define endpoints e aplica validações de entrada

### Boas Práticas Implementadas

- ✅ Separação de responsabilidades
- ✅ Validação de dados de entrada
- ✅ Tratamento centralizado de erros
- ✅ Código documentado
- ✅ IDs únicos (UUID)
- ✅ Validações de negócio

---

## 🚧 Próximos Passos

### Melhorias Sugeridas

1. **Banco de Dados**
   - Migrar de arquivo JSON para banco de dados (PostgreSQL, MySQL, MongoDB)
   - Implementar migrations
   - Adicionar ORM ou query builder (TypeORM, Sequelize, Prisma, Knex)

2. **Segurança**
   - Implementar autenticação (JWT)
   - Adicionar autorização (RBAC)
   - Implementar rate limiting
   - Configurar CORS adequadamente
   - Adicionar validação de entrada mais robusta

3. **Testes**
   - Testes unitários (Jest)
   - Testes de integração (Supertest)
   - Testes de carga
   - Cobertura de código

4. **Documentação**
   - Swagger/OpenAPI
   - Postman Collection
   - Diagramas de arquitetura

5. **DevOps**
   - CI/CD pipeline
   - Docker e Docker Compose
   - Deploy automatizado
   - Monitoramento e logging

6. **Funcionalidades**
   - Paginação na listagem
   - Filtros e busca
   - Ordenação
   - Soft delete
   - Histórico de alterações
   - Upload de imagens

---

## 🐛 Problemas Comuns

### Erro: "argument handler must be a function"

**Causa**: O arquivo de rotas não está exportando um Router corretamente.

**Solução**: Verifique se `productsRoutes.js` termina com `module.exports = router;`

### Erro: Permissões de escrita em `data/products.json`

**Causa**: Falta de permissões de escrita no arquivo ou diretório.

**Solução**: 
- Verifique as permissões do arquivo no Windows
- Certifique-se de que o diretório `data/` existe
- Execute o terminal como administrador se necessário

### Erro: Porta já em uso

**Causa**: A porta 3000 já está sendo usada por outro processo.

**Solução**: 
- Altere a porta usando a variável de ambiente: `PORT=3001 npm start`
- Ou encerre o processo que está usando a porta 3000

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

## 👤 Autor

**Renato Saldanha**

---

## 📝 Histórico de Versões

- **1.0.0** - Versão inicial
  - Implementação completa do CRUD
  - Validações de entrada
  - Arquitetura Repository + Service Layer
  - Persistência em arquivo JSON

---

**Desenvolvido com ❤️ usando Node.js e Express**


