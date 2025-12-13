# C4 Model - Level 3: Components (Backend)

## Backend API - Component Diagram

### Descrição
Este diagrama mostra os componentes internos do Backend API Application e como eles interagem.

---

## Diagrama

```
                         Frontend Web App
                                │
                                │ HTTP/REST
                                ▼
               ┌────────────────────────────────────┐
               │      API LAYER (FastAPI)           │
               │  ┌──────────────────────────────┐  │
               │  │   API Router (main.py)       │  │
               │  │   - CORS middleware          │  │
               │  │   - Exception handlers       │  │
               │  └────────────┬─────────────────┘  │
               │               │                     │
               │  ┌────────────▼─────────────────┐  │
               │  │   API v1 Routers             │  │
               │  │   ┌────────────────────┐     │  │
               │  │   │ auth.py            │     │  │
               │  │   │ - /register        │     │  │
               │  │   │ - /login           │     │  │
               │  │   │ - /logout          │     │  │
               │  │   └────────────────────┘     │  │
               │  │   ┌────────────────────┐     │  │
               │  │   │ tickets.py         │     │  │
               │  │   │ - CRUD tickets     │     │  │
               │  │   │ - messages         │     │  │
               │  │   └────────────────────┘     │  │
               │  │   ┌────────────────────┐     │  │
               │  │   │ chats.py           │     │  │
               │  │   │ - sessions         │     │  │
               │  │   │ - accept/messages  │     │  │
               │  │   └────────────────────┘     │  │
               │  │   ┌────────────────────┐     │  │
               │  │   │ knowledge.py       │     │  │
               │  │   │ - CRUD articles    │     │  │
               │  │   │ - search/helpful   │     │  │
               │  │   └────────────────────┘     │  │
               │  └─────────────┬────────────────┘  │
               │                │                    │
               │  ┌─────────────▼────────────────┐  │
               │  │   Dependencies (deps.py)     │  │
               │  │   - get_current_user()       │  │
               │  │   - get_current_active_user()│  │
               │  │   - get_db()                 │  │
               │  └──────────────┬───────────────┘  │
               └─────────────────┼───────────────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
        ▼                        ▼                        ▼
┌───────────────┐      ┌─────────────────┐      ┌────────────────┐
│  CORE LAYER   │      │  SCHEMAS LAYER  │      │  MODELS LAYER  │
│               │      │                 │      │                │
│  config.py    │      │  schemas.py     │      │  models.py     │
│  - Settings   │      │  - UserCreate   │      │  - User        │
│  - Env vars   │      │  - TicketCreate │      │  - Ticket      │
│               │      │  - Validation   │      │  - Message     │
│  security.py  │      │  - DTOs         │      │  - ChatSession │
│  - JWT create │      │                 │      │  - Article     │
│  - JWT decode │      │                 │      │                │
│  - Password   │      │                 │      │  Relationships │
│    hash       │      │                 │      │  Enums         │
└───────────────┘      └─────────────────┘      └────────┬───────┘
                                                          │
                                                          │
                                                ┌─────────▼────────┐
                                                │   DB LAYER       │
                                                │                  │
                                                │  session.py      │
                                                │  - Engine        │
                                                │  - SessionLocal  │
                                                │  - get_db()      │
                                                │                  │
                                                └─────────┬────────┘
                                                          │
                                ┌─────────────────────────┼────────────────┐
                                │                         │                │
                                ▼                         ▼                ▼
                         PostgreSQL                    Redis          (Future)
                         Database                     Cache           SMTP
```

---

## Componentes

### 1. API Layer

#### Main Application (main.py)
**Responsabilidade**: Entry point, configuração global

```python
app = FastAPI(
    title="SaaS de Suporte ao Cliente",
    version="1.0.0",
    docs_url="/api/docs"
)

# Middleware
app.add_middleware(CORSMiddleware, ...)

# Include routers
app.include_router(api_router, prefix="/api/v1")
```

**Features:**
- CORS middleware
- Exception handlers globais
- Health check endpoint
- OpenAPI configuration

---

#### API v1 Routers

**auth.py** - Autenticação
```
POST /api/v1/auth/register
POST /api/v1/auth/login
POST /api/v1/auth/logout
```

**tickets.py** - Sistema de Tickets
```
GET    /api/v1/tickets/
POST   /api/v1/tickets/
GET    /api/v1/tickets/{id}
PATCH  /api/v1/tickets/{id}
DELETE /api/v1/tickets/{id}
GET    /api/v1/tickets/{id}/messages
POST   /api/v1/tickets/{id}/messages
```

**chats.py** - Chat ao Vivo
```
POST   /api/v1/chats/
GET    /api/v1/chats/
GET    /api/v1/chats/waiting
POST   /api/v1/chats/{id}/accept
GET    /api/v1/chats/{id}/messages
POST   /api/v1/chats/{id}/messages
```

**knowledge.py** - Base de Conhecimento
```
GET    /api/v1/knowledge/
POST   /api/v1/knowledge/
GET    /api/v1/knowledge/{id}
PATCH  /api/v1/knowledge/{id}
DELETE /api/v1/knowledge/{id}
POST   /api/v1/knowledge/{id}/helpful
GET    /api/v1/knowledge/categories/list
```

---

#### Dependencies (deps.py)
**Responsabilidade**: Dependency injection

**Funções:**

`get_db()` - Database session
```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

`get_current_user()` - Autenticação
```python
async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    # Valida JWT e retorna usuário
```

`get_current_active_user()` - Verifica ativo
```python
async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    if not current_user.is_active:
        raise HTTPException(...)
    return current_user
```

---

### 2. Core Layer

#### config.py - Configurações
**Responsabilidade**: Settings centralizadas

```python
class Settings(BaseSettings):
    APP_NAME: str
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REDIS_URL: str
    
    class Config:
        env_file = ".env"

settings = Settings()
```

---

#### security.py - Segurança
**Responsabilidade**: Funções de autenticação

**Funções:**

`get_password_hash()` - Hash senhas
```python
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
```

`verify_password()` - Verifica senha
```python
def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
```

`create_access_token()` - Gera JWT
```python
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=...)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
```

`decode_access_token()` - Valida JWT
```python
def decode_access_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except JWTError:
        return None
```

---

### 3. Schemas Layer

#### schemas.py - DTOs (Data Transfer Objects)
**Responsabilidade**: Validação de entrada/saída

**User Schemas:**
```python
class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str = Field(..., min_length=8)
    role: str = "customer"

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    is_active: bool
    
    class Config:
        from_attributes = True
```

**Ticket Schemas:**
```python
class TicketCreate(BaseModel):
    title: str = Field(..., min_length=5)
    description: str = Field(..., min_length=10)
    priority: str = "medium"
    category: Optional[str] = None

class TicketResponse(TicketCreate):
    id: int
    status: str
    customer_id: int
    assigned_to: Optional[int]
    created_at: datetime
    # ...
```

---

### 4. Models Layer

#### models.py - SQLAlchemy Models
**Responsabilidade**: Estrutura do banco de dados

**Principais modelos:**

```python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    role = Column(Enum(UserRole))
    # Relationships
    tickets_created = relationship("Ticket", ...)

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    status = Column(Enum(TicketStatus))
    customer_id = Column(Integer, ForeignKey("users.id"))
    # ...

class Message(Base):
    __tablename__ = "messages"
    # ...

class ChatSession(Base):
    __tablename__ = "chat_sessions"
    # ...

class KnowledgeArticle(Base):
    __tablename__ = "knowledge_articles"
    # ...
```

**Enums:**
```python
class UserRole(str, enum.Enum):
    ADMIN = "admin"
    AGENT = "agent"
    CUSTOMER = "customer"

class TicketStatus(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    # ...
```

---

### 5. Database Layer

#### session.py - Database Connection
**Responsabilidade**: Gerenciar conexões

```python
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.DEBUG
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

## Fluxo de Request

### Exemplo: POST /api/v1/tickets/

```
1. Request HTTP chega → FastAPI (main.py)
2. CORS middleware → valida origem
3. Router tickets.py → função create_ticket()
4. Dependency Injection:
   - get_db() → fornece session
   - get_current_active_user() → valida JWT
5. Pydantic → valida TicketCreate
6. SQLAlchemy → cria Ticket model
7. db.add(ticket) → INSERT no PostgreSQL
8. db.commit() → confirma transação
9. Pydantic → converte para TicketResponse
10. FastAPI → retorna JSON response
```

---

## Padrões de Design

### 1. Dependency Injection
FastAPI usa para fornecer dependencies:
- Database sessions
- Usuário atual autenticado
- Configurações

### 2. Repository Pattern (implícito)
SQLAlchemy models servem como repositories

### 3. DTO Pattern
Schemas Pydantic separam dados externos de internos

### 4. Middleware Pattern
CORS e exception handling como middlewares

---

## Decisões Arquiteturais Relacionadas
- [ADR 001: FastAPI Backend](../adr/001-escolha-fastapi-backend.md)
- [ADR 003: JWT Authentication](../adr/003-autenticacao-jwt.md)
- [ADR 006: Estrutura Modular](../adr/006-estrutura-modular-backend.md)

---

**Versão**: 1.0
**Data**: 2024-12-07
**Autores**: Backend Developer, Software Architect

