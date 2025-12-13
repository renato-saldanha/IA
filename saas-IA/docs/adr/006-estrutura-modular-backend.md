# ADR 006: Estrutura Modular do Backend (Clean Architecture)

## Status
**Aceito** - 2024-12-07

## Decisores
- Tech Lead
- Backend Developer
- Software Architect

## Contexto

O backend do sistema de suporte ao cliente cresce em complexidade com múltiplas features (tickets, chat, knowledge base). Precisamos de uma estrutura organizacional que:

- Separe responsabilidades claramente
- Facilite manutenção e evolução
- Permita testes isolados
- Seja compreensível para novos desenvolvedores
- Siga boas práticas da indústria
- Escale com o crescimento do projeto

### Alternativas Consideradas:
1. **Clean Architecture (Camadas)** - Separação por responsabilidade
2. **Feature-based** - Organização por funcionalidade
3. **Flat structure** - Todos arquivos em poucos diretórios
4. **Domain-Driven Design (DDD)** - Organização por domínio

## Decisão

Escolhemos **Clean Architecture com camadas** para organizar o backend.

### Justificativa:

**Estrutura escolhida:**
```
backend/
├── app/
│   ├── api/          # Camada de apresentação (routers)
│   │   ├── deps.py   # Dependências (auth, db)
│   │   └── v1/       # Versão da API
│   │       ├── auth.py
│   │       ├── tickets.py
│   │       ├── chats.py
│   │       └── knowledge.py
│   ├── core/         # Configurações e utilitários centrais
│   │   ├── config.py
│   │   └── security.py
│   ├── db/           # Camada de dados
│   │   └── session.py
│   ├── models/       # Modelos do banco (SQLAlchemy)
│   │   └── models.py
│   └── schemas/      # Schemas de validação (Pydantic)
│       └── schemas.py
├── main.py           # Entry point
└── requirements.txt
```

**Princípios aplicados:**

1. **Separation of Concerns**: Cada camada tem responsabilidade única
2. **Dependency Inversion**: Camadas superiores dependem de abstrações
3. **Single Responsibility**: Cada módulo tem uma razão para mudar
4. **DRY** (Don't Repeat Yourself): Código reutilizável em `core/`

**Por que não Feature-based:**
- Para projeto deste tamanho, camadas são mais simples
- Features compartilham muitos modelos (User usado em tudo)
- Reuso de código seria mais difícil

**Por que não Flat structure:**
- Escalabilidade limitada
- Difícil encontrar código específico
- Mistura de responsabilidades

**Por que não DDD completo:**
- Overhead para projeto de médio porte
- Agregados e bounded contexts desnecessários inicialmente
- Podemos evoluir para DDD se necessário

## Consequências

### Positivas:
- ✅ **Manutenibilidade**: Fácil encontrar e modificar código
- ✅ **Testabilidade**: Cada camada pode ser testada isoladamente
- ✅ **Escalabilidade**: Adicionar features sem bagunça
- ✅ **Onboarding**: Estrutura clara para novos devs
- ✅ **Separation**: API, business logic, data access separados
- ✅ **Versionamento**: API v1, v2 facilmente gerenciáveis
- ✅ **Reuso**: Core e schemas reutilizáveis

### Negativas:
- ⚠️ **Boilerplate**: Mais arquivos que estrutura flat
- ⚠️ **Navigation**: Mais cliques para navegar entre camadas
- ⚠️ **Over-engineering**: Pode ser demais para projeto muito pequeno

### Riscos Mitigados:
- IDE com boa navegação (VSCode, PyCharm)
- Imports absolutos (`from app.models import User`)
- Documentação clara da estrutura

## Descrição das Camadas

### 1. API Layer (`app/api/`)
**Responsabilidade**: Endpoints HTTP, validação de entrada, resposta HTTP

```python
# app/api/v1/tickets.py
from fastapi import APIRouter, Depends
from app.schemas.schemas import TicketCreate, TicketResponse
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/", response_model=TicketResponse)
async def create_ticket(
    ticket_data: TicketCreate,
    current_user = Depends(get_current_user)
):
    # Lógica de criação
    pass
```

**Características:**
- Usa Pydantic schemas para validação
- Dependency injection para auth
- Status codes HTTP apropriados
- Documentação OpenAPI automática

### 2. Core Layer (`app/core/`)
**Responsabilidade**: Configurações, segurança, utilitários centrais

```python
# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str
    DATABASE_URL: str
    SECRET_KEY: str
    
    class Config:
        env_file = ".env"

settings = Settings()
```

**Características:**
- Settings centralizadas
- Funções de segurança (JWT, hashing)
- Constantes globais
- Utilitários reutilizáveis

### 3. Database Layer (`app/db/`)
**Responsabilidade**: Conexão com banco, sessões

```python
# app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**Características:**
- Engine do SQLAlchemy
- Session management
- Connection pooling
- Dependency para FastAPI

### 4. Models Layer (`app/models/`)
**Responsabilidade**: Modelos do banco de dados (ORM)

```python
# app/models/models.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    # ...
```

**Características:**
- Definições SQLAlchemy
- Relacionamentos entre tabelas
- Índices e constraints
- Enums

### 5. Schemas Layer (`app/schemas/`)
**Responsabilidade**: Validação de entrada/saída (DTOs)

```python
# app/schemas/schemas.py
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
class UserResponse(BaseModel):
    id: int
    email: str
    
    class Config:
        from_attributes = True
```

**Características:**
- Pydantic models
- Validação automática
- Serialização/deserialização
- Documentação OpenAPI

## Fluxo de Dados

```
Request HTTP
    ↓
API Router (app/api/v1/)
    ↓
Valida com Schema (app/schemas/)
    ↓
Autentica (app/api/deps.py)
    ↓
Acessa Model (app/models/)
    ↓
Consulta Database (app/db/)
    ↓
Retorna Schema (app/schemas/)
    ↓
Response HTTP
```

## Versionamento de API

Estrutura permite múltiplas versões:

```
app/api/
├── v1/           # Versão 1 (atual)
│   ├── auth.py
│   └── tickets.py
└── v2/           # Futuro: Versão 2
    └── tickets.py
```

Rotas:
- `/api/v1/tickets/`
- `/api/v2/tickets/` (futuro)

## Padrões de Código

### Naming Conventions:
- **Arquivos**: snake_case (tickets.py, user_schema.py)
- **Classes**: PascalCase (User, TicketCreate)
- **Funções**: snake_case (create_ticket, get_user)
- **Variáveis**: snake_case (user_id, ticket_list)
- **Constantes**: UPPER_CASE (SECRET_KEY, DATABASE_URL)

### Imports:
```python
# Imports absolutos (preferidos)
from app.models.models import User
from app.schemas.schemas import UserCreate
from app.core.config import settings

# Evitar imports relativos
# from ..models import User  # ❌
```

## Alternativas Consideradas

| Estrutura | Prós | Contras | Decisão |
|-----------|------|---------|---------|
| Clean Architecture | Clara, testável, escalável | Mais arquivos | ✅ Escolhido |
| Feature-based | Coeso por feature | Reuso difícil | ❌ Rejeitado |
| Flat | Simples | Não escala | ❌ Rejeitado |
| DDD completo | Modelagem rica | Overhead | ❌ Rejeitado |

## Evolução Futura

Possíveis melhorias:
- [ ] Service layer (`app/services/`) para business logic complexa
- [ ] Repository pattern (`app/repositories/`) para queries
- [ ] Use cases (`app/use_cases/`) para casos de uso específicos
- [ ] Events (`app/events/`) para event-driven architecture
- [ ] CQRS para separar reads/writes (se necessário)

## Referências
- [Clean Architecture by Uncle Bob](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices)
- [SQLAlchemy Organization Patterns](https://docs.sqlalchemy.org/en/20/orm/extensions/declarative/mixins.html)

## Notas de Implementação
- Imports absolutos configurados no Python path
- Type hints em todas funções
- Docstrings em classes e funções públicas
- Logging estruturado
- Tratamento de erros consistente

