# ADR 005: Next.js com App Router para Frontend

## Status
**Aceito** - 2024-12-07

## Decisores
- Frontend Developer
- Tech Lead
- UI/UX Designer

## Contexto

O frontend do sistema de suporte ao cliente requer uma interface moderna, responsiva e performática. Precisamos de uma solução que:

- Suporte Server-Side Rendering (SSR) para SEO
- Renderização do lado do cliente para interatividade
- Roteamento file-based para organização
- TypeScript para type safety
- Performance otimizada (Core Web Vitals)
- Developer experience excepcional
- Deploy simples (Vercel)

### Alternativas Consideradas:
1. **Next.js (App Router)** - Framework React com SSR
2. **Next.js (Pages Router)** - Versão anterior do Next.js
3. **Create React App** - Setup React tradicional
4. **Vite + React** - Build tool moderno
5. **Remix** - Framework React fullstack

## Decisão

Escolhemos **Next.js 15 com App Router** como framework frontend.

### Justificativa:

**Vantagens do Next.js App Router:**
- **Server Components**: React Server Components por padrão (performance)
- **Streaming SSR**: Carregamento progressivo de páginas
- **File-based routing**: Estrutura de pastas = rotas
- **Layouts aninhados**: Compartilhamento de UI entre páginas
- **Loading/Error states**: Tratamento automático
- **Route Groups**: Organização sem afetar URLs `(auth)`, `(dashboard)`
- **API Routes**: Backend endpoints no mesmo projeto (se necessário)
- **Image optimization**: Next/Image otimiza automaticamente
- **Font optimization**: Next/Font elimina layout shift
- **TypeScript nativo**: Suporte de primeira classe
- **Vercel deploy**: Deploy em 1 clique

**Por que App Router e não Pages Router:**
- App Router é o futuro do Next.js
- Server Components = melhor performance
- Layouts mais flexíveis
- Suspense boundaries melhores
- Data fetching mais simples

**Por que não Create React App:**
- Sem SSR/SSG nativo
- SEO limitado
- Performance inferior
- Build config manual
- Projeto deprecated pelo React team

**Por que não Vite + React:**
- SSR requer configuração manual complexa
- Sem file-based routing
- Sem otimizações automáticas
- Mais boilerplate

**Por que não Remix:**
- Comunidade menor
- Menos recursos de otimização
- Deploy menos estabelecido
- Curva de aprendizado

## Consequências

### Positivas:
- ✅ **Performance**: Server Components reduzem bundle JavaScript
- ✅ **SEO**: SSR garante indexação perfeita
- ✅ **DX**: Developer Experience excepcional
- ✅ **Type safety**: TypeScript em todo lugar
- ✅ **Otimizações**: Imagens, fontes, bundle splitting automáticos
- ✅ **Layouts**: Compartilhar navbar/sidebar facilmente
- ✅ **Loading states**: Suspense e streaming SSR
- ✅ **Deploy**: Vercel deploy otimizado

### Negativas:
- ⚠️ **Curva de aprendizado**: App Router é novo, requer adaptação
- ⚠️ **Server Components**: Conceito novo, pode confundir
- ⚠️ **Cache complexo**: Sistema de cache do Next.js requer compreensão
- ⚠️ **Breaking changes**: App Router ainda evoluindo

### Riscos Mitigados:
- Next.js é mantido pela Vercel (empresa bem financiada)
- Comunidade massiva e ativa
- Documentação excelente
- Casos de uso similares bem documentados

## Estrutura de Rotas

### Organização com Route Groups:

```
app/
├── layout.tsx                 # Root layout
├── page.tsx                   # Home page (/)
├── globals.css                # Estilos globais
│
├── (auth)/                    # Route group (não afeta URL)
│   ├── login/
│   │   └── page.tsx          # /login
│   └── register/
│       └── page.tsx          # /register
│
└── (dashboard)/               # Route group (não afeta URL)
    ├── layout.tsx            # Dashboard layout (sidebar)
    ├── tickets/
    │   ├── page.tsx          # /tickets
    │   ├── [id]/
    │   │   └── page.tsx      # /tickets/[id]
    │   └── new/
    │       └── page.tsx      # /tickets/new
    ├── chats/
    │   └── page.tsx          # /chats
    └── knowledge/
        └── page.tsx          # /knowledge
```

### Vantagens dessa estrutura:
- Route groups não afetam URLs
- Layouts compartilhados apenas onde necessário
- Fácil adicionar middleware por grupo
- Organização visual clara

## Stack Técnico Frontend

### Core:
- **Next.js 15**: Framework React
- **React 18**: Biblioteca UI
- **TypeScript**: Type safety

### Styling:
- **Tailwind CSS**: Utility-first CSS
- **Shadcn/ui**: Componentes acessíveis (planejado)
- **Lucide React**: Ícones modernos

### State Management:
- **React Query**: Server state (planejado)
- **Zustand**: Client state (se necessário)
- **React Hook Form**: Forms

### Validação:
- **Zod**: Schema validation

### HTTP Client:
- **Axios**: API requests

## Features Utilizadas

### 1. Server Components (RSC)
```tsx
// app/tickets/page.tsx
async function TicketsPage() {
  // Fetch no servidor, sem JavaScript no cliente
  const tickets = await fetchTickets()
  
  return <TicketList tickets={tickets} />
}
```

### 2. Layouts Aninhados
```tsx
// app/(dashboard)/layout.tsx
export default function DashboardLayout({ children }) {
  return (
    <div>
      <Sidebar />
      <main>{children}</main>
    </div>
  )
}
```

### 3. Loading States
```tsx
// app/(dashboard)/tickets/loading.tsx
export default function Loading() {
  return <Skeleton />
}
```

### 4. Error Boundaries
```tsx
// app/(dashboard)/tickets/error.tsx
export default function Error({ error, reset }) {
  return (
    <div>
      <h2>Algo deu errado!</h2>
      <button onClick={reset}>Tentar novamente</button>
    </div>
  )
}
```

## Performance

### Core Web Vitals alvos:
- **LCP** (Largest Contentful Paint): < 2.5s
- **FID** (First Input Delay): < 100ms
- **CLS** (Cumulative Layout Shift): < 0.1

### Otimizações:
- Image optimization automática
- Font optimization (next/font)
- Code splitting automático
- Prefetch em Link hover
- Static generation onde possível
- ISR (Incremental Static Regeneration) para conteúdo dinâmico

## Alternativas Consideradas

| Framework | Prós | Contras | Decisão |
|-----------|------|---------|---------|
| Next.js App Router | SSR, RSC, performance, DX | Curva aprendizado | ✅ Escolhido |
| Next.js Pages | Maduro, estável | Sem RSC, layout limitado | ❌ Rejeitado |
| CRA | Simples | Sem SSR, deprecated | ❌ Rejeitado |
| Vite + React | Rápido build | SSR manual | ❌ Rejeitado |
| Remix | Bom DX | Menor comunidade | ❌ Rejeitado |

## Configuração

### next.config.js:
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
  },
  experimental: {
    serverActions: {
      bodySizeLimit: '2mb'
    }
  }
}

module.exports = nextConfig
```

### tsconfig.json:
- `strict: true` para type safety máximo
- Paths configurados: `@/*` = raiz do projeto

## Referências
- [Next.js 15 Documentation](https://nextjs.org/docs)
- [React Server Components](https://react.dev/blog/2023/03/22/react-labs-what-we-have-been-working-on-march-2023#react-server-components)
- [App Router Migration Guide](https://nextjs.org/docs/app/building-your-application/upgrading/app-router-migration)
- [Next.js Performance](https://nextjs.org/docs/app/building-your-application/optimizing)

## Notas de Implementação
- Versão: Next.js 15.0.0
- React: 18.3.1
- TypeScript: 5.3.3
- Node.js: 20 LTS
- Package manager: npm

