# ADR 003: Autenticação JWT para APIs RESTful

## Status
**Aceito** - 2024-12-07

## Decisores
- Security Engineer
- Backend Developer
- Tech Lead

## Contexto

O sistema de suporte ao cliente requer autenticação e autorização para três tipos de usuários: Clientes, Agentes e Administradores. Cada tipo tem permissões diferentes para acessar tickets, chats e base de conhecimento.

### Requisitos de Autenticação:
- Autenticação stateless para APIs REST
- Suporte a múltiplos dispositivos simultâneos
- Tokens de curta duração para segurança
- Renovação de tokens sem re-login
- Suporte a roles/permissões (RBAC)
- Performance em alta concorrência
- Compatibilidade com frontend SPA (Next.js)

### Alternativas Consideradas:
1. **JWT (JSON Web Tokens)** - Tokens autocontidos e stateless
2. **Session-based auth** - Sessões armazenadas no servidor
3. **OAuth2** - Protocolo de autorização delegada
4. **API Keys** - Chaves estáticas por usuário

## Decisão

Escolhemos **JWT (JSON Web Tokens)** como mecanismo de autenticação.

### Justificativa:

**Vantagens do JWT:**
- **Stateless**: Não requer armazenamento de sessões no servidor
- **Escalável**: Fácil escalar horizontalmente sem sessão compartilhada
- **Cross-domain**: Funciona perfeitamente em arquiteturas SPA/API separadas
- **Autocontido**: Token carrega informações do usuário (email, role)
- **Performance**: Validação rápida sem consulta ao banco
- **Padrão da indústria**: Amplamente suportado e testado
- **Mobile-friendly**: Ideal para futuras aplicações mobile

**Por que não Session-based:**
- Requer Redis/Memcached para compartilhar sessões
- Dificuldade em escalar horizontalmente
- CSRF tokens necessários
- Não funciona bem com múltiplos domínios/subdomínios

**Por que não OAuth2:**
- Overhead desnecessário para autenticação interna
- OAuth2 é para autorização delegada (login com Google/Facebook)
- Complexidade adicional sem benefício
- Podemos adicionar OAuth2 futuramente se necessário

**Por que não API Keys:**
- Não expira automaticamente
- Difícil rotacionar
- Sem contexto de usuário incorporado
- Melhor para integrações máquina-a-máquina

## Consequências

### Positivas:
- ✅ **Escalabilidade**: Stateless permite múltiplos servidores sem sincronização
- ✅ **Performance**: Sem consulta ao banco/Redis em cada request
- ✅ **Segurança**: Tokens expiram automaticamente (24h)
- ✅ **Flexibilidade**: Suporta refresh tokens se necessário
- ✅ **Developer-friendly**: Bibliotecas maduras (python-jose, JWT.io)
- ✅ **Debugging**: Tokens podem ser inspecionados em jwt.io
- ✅ **Mobile-ready**: Preparado para futuras apps mobile

### Negativas:
- ⚠️ **Revogação complexa**: Não há blacklist nativa de tokens
- ⚠️ **Tamanho**: Tokens JWT são maiores que session IDs
- ⚠️ **Dados sensíveis**: Não devemos colocar dados sensíveis no payload
- ⚠️ **XSS vulnerability**: Requer cuidado no armazenamento (localStorage vs httpOnly cookies)

### Riscos Mitigados:
- **Revogação**: Implementar token versioning no banco se necessário
- **Expiração curta**: Tokens expiram em 24h
- **HTTPS only**: Tokens nunca trafegam sem TLS
- **Secret key**: Chave forte e rotacionada periodicamente
- **Validação rigorosa**: Verificar signature, expiration, issuer

## Implementação

### Estrutura do Token JWT:

```json
{
  "sub": "user@email.com",
  "exp": 1704672000,
  "iat": 1704585600,
  "type": "access"
}
```

### Configuração de Segurança:

```python
# Settings
SECRET_KEY = "strong-random-key-256-bits"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours
```

### Fluxo de Autenticação:

1. **Login**: POST `/api/v1/auth/login`
   - Valida email/senha
   - Gera JWT token
   - Retorna token ao cliente

2. **Requests autenticadas**:
   - Cliente envia: `Authorization: Bearer <token>`
   - Backend valida signature e expiration
   - Extrai user info do payload
   - Autoriza baseado no role

3. **Logout**:
   - Cliente descarta o token
   - (Opcional) Server registra logout para auditoria

### Roles e Permissões:

| Role | Permissões |
|------|------------|
| **customer** | Ver próprios tickets/chats, acessar base de conhecimento |
| **agent** | Ver todos tickets/chats, criar artigos, responder tickets |
| **admin** | Todas permissões + deletar tickets/artigos, gerenciar usuários |

## Alternativas Consideradas

| Método | Prós | Contras | Decisão |
|--------|------|---------|---------|
| JWT | Stateless, escalável, padrão | Revogação complexa | ✅ Escolhido |
| Sessions | Revogação fácil, simples | Requer storage, não escala | ❌ Rejeitado |
| OAuth2 | Padrão delegação | Complexo, desnecessário | ❌ Rejeitado |
| API Keys | Simples | Não expira, sem contexto | ❌ Rejeitado |

## Segurança Adicional

### Boas Práticas Implementadas:
- ✅ Senhas hasheadas com bcrypt (cost=12)
- ✅ Tokens só via HTTPS em produção
- ✅ CORS configurado adequadamente
- ✅ Rate limiting no endpoint de login
- ✅ Validação de input com Pydantic
- ✅ Logs de autenticação para auditoria

### Futuras Melhorias:
- [ ] Refresh tokens para renovação automática
- [ ] MFA (Multi-Factor Authentication)
- [ ] IP whitelisting para admins
- [ ] Device tracking e notificações
- [ ] Token blacklist em Redis para logout forçado

## Referências
- [JWT.io - Introduction](https://jwt.io/introduction)
- [OWASP JWT Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html)
- [python-jose Documentation](https://python-jose.readthedocs.io/)
- [RFC 7519 - JWT Specification](https://datatracker.ietf.org/doc/html/rfc7519)

## Notas de Implementação
- Biblioteca: python-jose[cryptography]
- Password hashing: passlib[bcrypt]
- Token storage (client): localStorage
- Expiration: 24 horas
- Header: `Authorization: Bearer <token>`

