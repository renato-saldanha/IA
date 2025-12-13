# Fluxo de Autenticação - Registro e Login

## Descrição
Este diagrama detalha o fluxo completo de autenticação do sistema, incluindo registro de novos usuários e login com JWT.

---

## 1. Fluxo de Registro

```
┌─────────┐                 ┌──────────┐                 ┌──────────┐
│ Cliente │                 │ Frontend │                 │ Backend  │
└────┬────┘                 └────┬─────┘                 └────┬─────┘
     │                           │                            │
     │ 1. Acessa /register       │                            │
     │──────────────────────────>│                            │
     │                           │                            │
     │ 2. Preenche formulário    │                            │
     │    - Email                │                            │
     │    - Nome                 │                            │
     │    - Senha                │                            │
     │    - Tipo (role)          │                            │
     │──────────────────────────>│                            │
     │                           │ 3. Valida client-side      │
     │                           │    - Email válido?         │
     │                           │    - Senha >= 8 chars?     │
     │                           │    - Senhas coincidem?     │
     │                           │                            │
     │                           │ 4. POST /api/v1/auth/register
     │                           │    {                       │
     │                           │      email,                │
     │                           │      full_name,            │
     │                           │      password,             │
     │                           │      role                  │
     │                           │    }                       │
     │                           │───────────────────────────>│
     │                           │                            │
     │                           │                            │ 5. Valida Pydantic
     │                           │                            │    UserCreate schema
     │                           │                            │
     │                           │                            │ 6. Verifica email único
     │                           │                            │    SELECT * FROM users
     │                           │                            │    WHERE email = ?
     │                           │                            │
     │                           │  [SE EMAIL JÁ EXISTE]      │
     │                           │<───────────────────────────┤
     │                           │  400 Bad Request           │
     │                           │  "Email já cadastrado"     │
     │<──────────────────────────┤                            │
     │  Mostra erro              │                            │
     │                           │                            │
     │                           │  [SE EMAIL DISPONÍVEL]     │
     │                           │                            │ 7. Hash senha (bcrypt)
     │                           │                            │    cost=12
     │                           │                            │
     │                           │                            │ 8. INSERT INTO users
     │                           │                            │    (email, full_name,
     │                           │                            │     hashed_password,
     │                           │                            │     role, is_active)
     │                           │                            │
     │                           │<───────────────────────────┤
     │                           │  201 Created               │
     │                           │  UserResponse {id, email...}│
     │<──────────────────────────┤                            │
     │  9. Mostra sucesso        │                            │
     │                           │ 10. Auto-login (opcional)  │
     │                           │     Chama /login           │
     │                           │                            │
     └───────────────────────────┴────────────────────────────┘
```

---

## 2. Fluxo de Login

```
┌─────────┐                 ┌──────────┐                 ┌──────────┐
│ Cliente │                 │ Frontend │                 │ Backend  │
└────┬────┘                 └────┬─────┘                 └────┬─────┘
     │                           │                            │
     │ 1. Acessa /login          │                            │
     │──────────────────────────>│                            │
     │                           │                            │
     │ 2. Insere credenciais     │                            │
     │    - Email                │                            │
     │    - Senha                │                            │
     │──────────────────────────>│                            │
     │                           │ 3. POST /api/v1/auth/login │
     │                           │    FormData:               │
     │                           │      username=email        │
     │                           │      password=senha        │
     │                           │───────────────────────────>│
     │                           │                            │
     │                           │                            │ 4. Busca usuário
     │                           │                            │    SELECT * FROM users
     │                           │                            │    WHERE email = ?
     │                           │                            │
     │                           │  [SE USUÁRIO NÃO EXISTE]   │
     │                           │<───────────────────────────┤
     │                           │  401 Unauthorized          │
     │                           │  "Email ou senha incorretos"│
     │<──────────────────────────┤                            │
     │  Mostra erro              │                            │
     │                           │                            │
     │                           │  [SE USUÁRIO EXISTE]       │
     │                           │                            │ 5. Verifica senha
     │                           │                            │    bcrypt.verify(
     │                           │                            │      plain_password,
     │                           │                            │      hashed_password
     │                           │                            │    )
     │                           │                            │
     │                           │  [SE SENHA INCORRETA]      │
     │                           │<───────────────────────────┤
     │                           │  401 Unauthorized          │
     │<──────────────────────────┤                            │
     │  Mostra erro              │                            │
     │                           │                            │
     │                           │  [SE SENHA CORRETA]        │
     │                           │                            │ 6. Verifica is_active
     │                           │                            │    
     │                           │  [SE NÃO ATIVO]            │
     │                           │<───────────────────────────┤
     │                           │  400 Bad Request           │
     │                           │  "Usuário inativo"         │
     │<──────────────────────────┤                            │
     │                           │                            │
     │                           │  [SE ATIVO]                │
     │                           │                            │ 7. Cria JWT token
     │                           │                            │    payload = {
     │                           │                            │      sub: email,
     │                           │                            │      exp: now+24h
     │                           │                            │    }
     │                           │                            │    token = jwt.encode()
     │                           │                            │
     │                           │                            │ 8. UPDATE users
     │                           │                            │    SET is_online=TRUE
     │                           │                            │
     │                           │<───────────────────────────┤
     │                           │  200 OK                    │
     │                           │  {                         │
     │                           │    access_token: "eyJ..." ,│
     │                           │    token_type: "bearer"    │
     │                           │  }                         │
     │                           │ 9. Salva token             │
     │                           │    localStorage.setItem(   │
     │                           │      'access_token',       │
     │                           │      token                 │
     │                           │    )                       │
     │                           │                            │
     │                           │ 10. Redirect               │
     │<──────────────────────────┤     /dashboard/tickets     │
     │  Acessa dashboard         │                            │
     │                           │                            │
     └───────────────────────────┴────────────────────────────┘
```

---

## 3. Fluxo de Request Autenticado

```
┌─────────┐                 ┌──────────┐                 ┌──────────┐
│ Cliente │                 │ Frontend │                 │ Backend  │
└────┬────┘                 └────┬─────┘                 └────┬─────┘
     │                           │                            │
     │ 1. Acessa página protegida│                            │
     │──────────────────────────>│ 2. Lê token do storage     │
     │                           │    token = localStorage    │
     │                           │            .getItem(...)   │
     │                           │                            │
     │                           │ 3. GET /api/v1/tickets/    │
     │                           │    Headers:                │
     │                           │      Authorization:        │
     │                           │        Bearer <token>      │
     │                           │───────────────────────────>│
     │                           │                            │
     │                           │                            │ 4. Extrai token
     │                           │                            │    do header
     │                           │                            │
     │                           │                            │ 5. Decodifica JWT
     │                           │                            │    payload = jwt
     │                           │                            │      .decode(token)
     │                           │                            │
     │                           │  [SE TOKEN INVÁLIDO/EXPIRADO]
     │                           │<───────────────────────────┤
     │                           │  401 Unauthorized          │
     │<──────────────────────────┤  "Credenciais inválidas"   │
     │  Redirect /login          │                            │
     │                           │                            │
     │                           │  [SE TOKEN VÁLIDO]         │
     │                           │                            │ 6. Extrai email
     │                           │                            │    email=payload['sub']
     │                           │                            │
     │                           │                            │ 7. Busca usuário
     │                           │                            │    SELECT * FROM users
     │                           │                            │    WHERE email = ?
     │                           │                            │
     │                           │                            │ 8. Verifica is_active
     │                           │                            │
     │                           │                            │ 9. Executa query
     │                           │                            │    (com current_user)
     │                           │                            │
     │                           │<───────────────────────────┤
     │                           │  200 OK                    │
     │                           │  [dados solicitados]       │
     │<──────────────────────────┤                            │
     │  Renderiza dados          │                            │
     │                           │                            │
     └───────────────────────────┴────────────────────────────┘
```

---

## 4. Fluxo de Logout

```
┌─────────┐                 ┌──────────┐                 ┌──────────┐
│ Cliente │                 │ Frontend │                 │ Backend  │
└────┬────┘                 └────┬─────┘                 └────┬─────┘
     │                           │                            │
     │ 1. Clica "Sair"           │                            │
     │──────────────────────────>│                            │
     │                           │ 2. POST /api/v1/auth/logout│
     │                           │    (com token no header)   │
     │                           │───────────────────────────>│
     │                           │                            │
     │                           │                            │ 3. Valida token
     │                           │                            │
     │                           │                            │ 4. UPDATE users
     │                           │                            │    SET is_online=FALSE
     │                           │                            │
     │                           │<───────────────────────────┤
     │                           │  200 OK                    │
     │                           │  "Logout realizado"        │
     │                           │                            │
     │                           │ 5. Remove token            │
     │                           │    localStorage            │
     │                           │      .removeItem('...')    │
     │                           │                            │
     │                           │ 6. Redirect /login         │
     │<──────────────────────────┤                            │
     │  Volta para login         │                            │
     │                           │                            │
     └───────────────────────────┴────────────────────────────┘
```

---

## Detalhes de Implementação

### JWT Token Structure
```json
{
  "sub": "user@email.com",
  "exp": 1704672000,
  "iat": 1704585600,
  "type": "access"
}
```

### Password Hashing
- **Algorithm**: bcrypt
- **Cost factor**: 12
- **Salt**: automático (bcrypt)

### Token Expiration
- **Duration**: 24 horas (1440 minutos)
- **Renewal**: Não implementado (v1.0)
- **Future**: Refresh tokens

### Security Headers
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## Error Handling

| Erro | Status Code | Mensagem |
|------|-------------|----------|
| Email já existe | 400 | "Email já cadastrado" |
| Credenciais inválidas | 401 | "Email ou senha incorretos" |
| Usuário inativo | 400 | "Usuário inativo" |
| Token inválido | 401 | "Não foi possível validar credenciais" |
| Token expirado | 401 | "Token expirado" |

---

## Decisões Arquiteturais Relacionadas
- [ADR 003: Autenticação JWT](../adr/003-autenticacao-jwt.md)

---

**Versão**: 1.0
**Data**: 2024-12-07
**Autores**: Backend Developer, Security Engineer

