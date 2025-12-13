# C4 Model - Level 3: Components (Frontend)

## Frontend Web Application - Component Diagram

### Descrição
Este diagrama mostra os componentes internos do Frontend Next.js e como eles interagem.

---

## Diagrama

```
                            Navegador do Usuário
                                     │
                                     │ HTTPS
                                     ▼
               ┌──────────────────────────────────────────┐
               │    NEXT.JS APPLICATION (Port 3000)       │
               │                                          │
               │  ┌────────────────────────────────────┐  │
               │  │    App Router                      │  │
               │  │                                    │  │
               │  │  layout.tsx (Root)                 │  │
               │  │  ├─ page.tsx (Home)                │  │
               │  │  ├─ (auth)/                        │  │
               │  │  │   ├─ login/page.tsx             │  │
               │  │  │   └─ register/page.tsx          │  │
               │  │  └─ (dashboard)/                   │  │
               │  │      ├─ layout.tsx (Dashboard)     │  │
               │  │      ├─ tickets/                   │  │
               │  │      │   └─ page.tsx               │  │
               │  │      ├─ chats/                     │  │
               │  │      │   └─ page.tsx               │  │
               │  │      └─ knowledge/                 │  │
               │  │          └─ page.tsx               │  │
               │  └─────────────────┬──────────────────┘  │
               │                    │                     │
               │  ┌─────────────────▼──────────────────┐  │
               │  │    Components Layer                │  │
               │  │                                    │  │
               │  │  components/                       │  │
               │  │  ├─ ui/           (Reusable UI)    │  │
               │  │  ├─ forms/        (Form components)│  │
               │  │  └─ layouts/      (Layout parts)   │  │
               │  └─────────────────┬──────────────────┘  │
               │                    │                     │
               │  ┌─────────────────▼──────────────────┐  │
               │  │    Library Layer                   │  │
               │  │                                    │  │
               │  │  lib/                              │  │
               │  │  ├─ api.ts        (API Client)     │  │
               │  │  │   - apiClient class             │  │
               │  │  │   - HTTP methods                │  │
               │  │  │   - Token management            │  │
               │  │  │                                 │  │
               │  │  └─ types.ts      (TypeScript)     │  │
               │  │      - User, Ticket               │  │
               │  │      - Message, Chat              │  │
               │  │      - Article types              │  │
               │  └─────────────────┬──────────────────┘  │
               │                    │                     │
               │  ┌─────────────────▼──────────────────┐  │
               │  │    Styling Layer                   │  │
               │  │                                    │  │
               │  │  - globals.css    (Tailwind base)  │  │
               │  │  - tailwind.config.ts              │  │
               │  │  - Utility classes                 │  │
               │  └────────────────────────────────────┘  │
               └───────────────────┬──────────────────────┘
                                   │
                                   │ HTTP/REST (JSON)
                                   ▼
                           Backend API (8000)
```

---

## Componentes

### 1. App Router Layer

#### Root Layout (app/layout.tsx)
**Responsabilidade**: Layout global da aplicação

```tsx
export default function RootLayout({ children }) {
  return (
    <html lang="pt-BR">
      <body className={inter.className}>
        {children}
      </body>
    </html>
  )
}
```

**Features:**
- Metadata (title, description)
- Fonte global (next/font)
- Styles globais

---

#### Home Page (app/page.tsx)
**Responsabilidade**: Landing page

**Features:**
- Hero section
- Feature showcase (Tickets, Chat, KB)
- CTA buttons
- Links para login/registro

---

#### Auth Route Group (app/(auth)/)
**Responsabilidade**: Páginas de autenticação

**login/page.tsx:**
```tsx
'use client'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  
  const handleSubmit = async (e) => {
    await apiClient.login({ email, password })
    router.push('/dashboard/tickets')
  }
  
  return <form onSubmit={handleSubmit}>...</form>
}
```

**register/page.tsx:**
- Formulário de registro
- Validação client-side
- Criação + login automático

**Features:**
- Formulários controlados
- Validação de inputs
- Error handling
- Loading states

---

#### Dashboard Route Group (app/(dashboard)/)
**Responsabilidade**: Área logada do sistema

**layout.tsx (Dashboard):**
```tsx
export default function DashboardLayout({ children }) {
  return (
    <div className="min-h-screen">
      <Navbar />
      <div className="flex">
        <Sidebar />
        <main className="flex-1 p-8">
          {children}
        </main>
      </div>
    </div>
  )
}
```

**Features:**
- Navbar compartilhada
- Sidebar com navegação
- Protected routes (auth check)

---

**tickets/page.tsx:**
```tsx
'use client'

export default function TicketsPage() {
  const [tickets, setTickets] = useState([])
  
  useEffect(() => {
    loadTickets()
  }, [])
  
  const loadTickets = async () => {
    const data = await apiClient.getTickets()
    setTickets(data)
  }
  
  return (
    <>
      <h1>Meus Tickets</h1>
      <TicketList tickets={tickets} />
    </>
  )
}
```

**Features:**
- Lista de tickets
- Filtros (status, prioridade)
- Link para criar ticket
- Badges de status/prioridade

---

**chats/page.tsx:**
- Lista de sessões de chat
- Iniciar novo chat
- Ver histórico

**knowledge/page.tsx:**
- Busca de artigos
- Lista por categoria
- Visualização de artigos

---

### 2. Components Layer

#### UI Components (components/ui/)
**Responsabilidade**: Componentes reutilizáveis

**Exemplos:**
```
Button.tsx       - Botões estilizados
Card.tsx         - Cards com shadow
Badge.tsx        - Status badges
Input.tsx        - Inputs de formulário
Modal.tsx        - Modais
Dropdown.tsx     - Dropdowns
Spinner.tsx      - Loading spinners
```

**Padrão:**
```tsx
interface ButtonProps {
  variant?: 'primary' | 'secondary'
  size?: 'sm' | 'md' | 'lg'
  children: React.ReactNode
  onClick?: () => void
}

export function Button({ 
  variant = 'primary', 
  size = 'md', 
  children, 
  onClick 
}: ButtonProps) {
  const classes = cn(
    baseClasses,
    variantClasses[variant],
    sizeClasses[size]
  )
  
  return (
    <button className={classes} onClick={onClick}>
      {children}
    </button>
  )
}
```

---

#### Form Components (components/forms/)
**Responsabilidade**: Formulários específicos

**Exemplos:**
```
LoginForm.tsx
RegisterForm.tsx
TicketForm.tsx
MessageForm.tsx
```

**Features:**
- React Hook Form
- Zod validation (planejado)
- Error messages
- Submit handling

---

#### Layout Components (components/layouts/)
**Responsabilidade**: Partes do layout

**Exemplos:**
```
Navbar.tsx       - Barra de navegação
Sidebar.tsx      - Menu lateral
Footer.tsx       - Rodapé
```

---

### 3. Library Layer

#### API Client (lib/api.ts)
**Responsabilidade**: Comunicação com backend

```typescript
class ApiClient {
  private client: AxiosInstance
  
  constructor() {
    this.client = axios.create({
      baseURL: `${API_URL}/api/v1`,
      headers: { 'Content-Type': 'application/json' }
    })
    
    // Interceptor para adicionar token
    this.client.interceptors.request.use((config) => {
      const token = this.getToken()
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }
      return config
    })
  }
  
  // Authentication
  async login(data: LoginRequest): Promise<TokenResponse>
  async register(data: RegisterRequest): Promise<User>
  async logout(): Promise<void>
  
  // Tickets
  async getTickets(params?): Promise<Ticket[]>
  async createTicket(data): Promise<Ticket>
  async updateTicket(id, data): Promise<Ticket>
  
  // Chats
  async createChatSession(): Promise<ChatSession>
  async sendChatMessage(id, data): Promise<Message>
  
  // Knowledge Base
  async getArticles(params?): Promise<KnowledgeArticle[]>
  async getArticle(id): Promise<KnowledgeArticle>
}

export const apiClient = new ApiClient()
```

**Features:**
- Axios instance configurado
- Token management (localStorage)
- Interceptors para auth
- Type-safe methods
- Error handling

---

#### Types (lib/types.ts)
**Responsabilidade**: TypeScript types

```typescript
export interface User {
  id: number
  email: string
  full_name: string
  role: 'admin' | 'agent' | 'customer'
  is_active: boolean
  is_online: boolean
}

export interface Ticket {
  id: number
  title: string
  description: string
  status: 'open' | 'in_progress' | 'waiting' | 'resolved' | 'closed'
  priority: 'low' | 'medium' | 'high' | 'urgent'
  customer_id: number
  assigned_to?: number
  created_at: string
}

// ... outros tipos
```

---

### 4. Styling Layer

#### Tailwind CSS
**Responsabilidade**: Estilização

**globals.css:**
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

**tailwind.config.ts:**
```typescript
const config: Config = {
  content: ['./app/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: { /* ... */ }
      }
    }
  }
}
```

**Uso:**
```tsx
<div className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl">
  <h2 className="text-2xl font-bold text-gray-900 mb-4">
    Título
  </h2>
</div>
```

---

## Data Flow

### Exemplo: Login do usuário

```
1. User digita email/senha → LoginPage (Client Component)
2. handleSubmit() → apiClient.login()
3. apiClient → POST /api/v1/auth/login → Backend
4. Backend retorna token → apiClient salva no localStorage
5. apiClient.setToken(token)
6. router.push('/dashboard/tickets') → Next.js navega
7. TicketsPage carrega → apiClient.getTickets()
8. apiClient adiciona token no header → GET /api/v1/tickets/
9. Backend valida token → retorna tickets
10. setTickets(data) → React re-renderiza → UI atualiza
```

---

## Padrões de Design

### 1. Component Composition
Componentes pequenos e reutilizáveis

### 2. Container/Presentational
- Container: Lógica e estado (pages)
- Presentational: UI pura (components)

### 3. Custom Hooks (planejado)
```tsx
function useAuth() {
  // Hook reutilizável para autenticação
}

function useTickets() {
  // Hook para gerenciar tickets
}
```

### 4. Client/Server Components
- Server Components: SEO, data fetching
- Client Components: Interatividade

---

## Decisões Arquiteturais Relacionadas
- [ADR 005: Next.js Frontend](../adr/005-frontend-nextjs-typescript.md)
- [ADR 008: Tailwind CSS](../adr/008-tailwind-css-styling.md)

---

**Versão**: 1.0
**Data**: 2024-12-07
**Autores**: Frontend Developer, UI/UX Designer

