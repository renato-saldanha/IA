# ADR 008: Tailwind CSS para Estilização

## Status
**Aceito** - 2024-12-07

## Decisores
- Frontend Developer
- UI/UX Designer
- Tech Lead

## Contexto

O frontend do sistema de suporte ao cliente precisa de uma solução de estilização que seja:

- Rápida de desenvolver
- Consistente em todo o projeto
- Responsiva por padrão
- Customizável para branding
- Performance otimizada
- Manutenível a longo prazo
- Compatível com Next.js

### Alternativas Consideradas:
1. **Tailwind CSS** - Utility-first CSS framework
2. **CSS Modules** - Scoped CSS nativo do Next.js
3. **Styled Components** - CSS-in-JS
4. **Emotion** - CSS-in-JS
5. **Sass/SCSS** - Preprocessador CSS tradicional

## Decisão

Escolhemos **Tailwind CSS** como solução de estilização.

### Justificativa:

**Vantagens do Tailwind CSS:**
- **Desenvolvimento rápido**: Classes utilitárias prontas
- **Consistência**: Design tokens padronizados (spacing, colors, fonts)
- **Responsivo**: Breakpoints mobile-first (`sm:`, `md:`, `lg:`)
- **Customização**: tailwind.config.ts para branding
- **Performance**: PurgeCSS remove CSS não usado
- **Sem naming**: Não precisa inventar nomes de classes
- **Intellisense**: Autocompletar no VS Code
- **Documentação**: Docs excelentes e searcháveis
- **Comunidade**: Massiva, muitos plugins

**Por que não CSS Modules:**
- Requer naming de classes
- Menos consistência (sem design tokens)
- Responsividade requer media queries manuais
- Mais boilerplate

**Por que não Styled Components:**
- Runtime overhead (CSS-in-JS)
- Problemas com Server Components
- Bundle size maior
- Performance inferior

**Por que não Emotion:**
- Mesmos problemas que Styled Components
- Menos adotado que SC ou Tailwind

**Por que não Sass/SCSS:**
- Requer naming de classes
- Menos opinativo sobre design
- Responsividade manual
- Sem purging automático

## Consequências

### Positivas:
- ✅ **Velocidade**: Prototipar 3x mais rápido
- ✅ **Consistência**: Spacing e colors padronizados
- ✅ **Responsivo**: Mobile-first por padrão
- ✅ **Performance**: CSS final ~10-20KB (após purge)
- ✅ **Manutenção**: Fácil identificar estilos no JSX
- ✅ **Dark mode**: Built-in com `dark:` variant
- ✅ **Plugins**: Ecosystem rico (forms, typography)
- ✅ **Zero-config**: Funciona com Next.js out-of-the-box

### Negativas:
- ⚠️ **HTML "sujo"**: Classes longas no markup
- ⚠️ **Curva de aprendizado**: Memorizar classes utility
- ⚠️ **Customização complexa**: Estilos muito específicos requerem workarounds
- ⚠️ **Build time**: Pequeno overhead no build

### Riscos Mitigados:
- Componentes reutilizáveis abstraem classes longas
- Intellisense ajuda com memorização
- @apply para estilos complexos (quando necessário)
- Tailwind official plugins para casos extremos

## Configuração

### tailwind.config.ts:
```typescript
import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          // ... cores customizadas
          900: '#0c4a6e',
        },
      },
    },
  },
  plugins: [],
}
export default config
```

### globals.css:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Custom utilities se necessário */
@layer utilities {
  .text-balance {
    text-wrap: balance;
  }
}
```

## Padrões de Uso

### 1. Componentes Básicos

**Button:**
```tsx
<button className="bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2">
  Criar Ticket
</button>
```

**Card:**
```tsx
<div className="bg-white rounded-lg shadow p-6 hover:shadow-xl transition-shadow">
  <h2 className="text-xl font-bold text-gray-900 mb-4">
    Título
  </h2>
  <p className="text-gray-600">
    Conteúdo
  </p>
</div>
```

### 2. Responsividade

```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  {/* Mobile: 1 col, Tablet: 2 cols, Desktop: 3 cols */}
</div>

<h1 className="text-2xl md:text-3xl lg:text-4xl font-bold">
  {/* Font size adapta por breakpoint */}
</h1>
```

### 3. Estados

```tsx
{/* Hover, Focus, Active */}
<button className="bg-blue-500 hover:bg-blue-600 focus:ring-2 active:bg-blue-700">

{/* Disabled */}
<button className="disabled:opacity-50 disabled:cursor-not-allowed" disabled>

{/* Group hover (parent hover afeta child) */}
<div className="group">
  <img className="group-hover:scale-110 transition-transform" />
</div>
```

### 4. Dark Mode (Futuro)

```tsx
<div className="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
  {/* Automático com class="dark" no <html> */}
</div>
```

## Componentização

Para evitar repetição, criamos componentes:

```tsx
// components/Button.tsx
interface ButtonProps {
  variant?: 'primary' | 'secondary'
  children: React.ReactNode
  onClick?: () => void
}

export function Button({ variant = 'primary', children, onClick }: ButtonProps) {
  const baseClasses = "px-4 py-2 rounded-md font-medium focus:outline-none focus:ring-2"
  
  const variantClasses = {
    primary: "bg-primary-600 text-white hover:bg-primary-700 focus:ring-primary-500",
    secondary: "bg-gray-200 text-gray-900 hover:bg-gray-300 focus:ring-gray-500"
  }
  
  return (
    <button 
      className={`${baseClasses} ${variantClasses[variant]}`}
      onClick={onClick}
    >
      {children}
    </button>
  )
}

// Uso:
<Button variant="primary">Criar Ticket</Button>
```

## Design System

### Cores:
- **Primary**: Azul (identidade da marca)
- **Success**: Verde (ações positivas)
- **Warning**: Amarelo (alertas)
- **Danger**: Vermelho (erros, deletar)
- **Gray**: Textos e backgrounds

### Spacing Scale:
Tailwind usa escala consistente:
- `p-1` = 0.25rem (4px)
- `p-2` = 0.5rem (8px)
- `p-4` = 1rem (16px)
- `p-6` = 1.5rem (24px)
- `p-8` = 2rem (32px)

### Typography:
- `text-xs` → `text-sm` → `text-base` → `text-lg` → `text-xl` → `text-2xl`
- Font weights: `font-normal`, `font-medium`, `font-semibold`, `font-bold`

### Breakpoints:
- `sm`: 640px (tablet pequeno)
- `md`: 768px (tablet)
- `lg`: 1024px (desktop)
- `xl`: 1280px (desktop grande)
- `2xl`: 1536px (desktop muito grande)

## Performance

### Purging:
Tailwind automaticamente remove classes não usadas:

**Antes do purge**: ~3.5MB CSS
**Depois do purge**: ~10-20KB CSS

### JIT Mode:
Just-In-Time compiler gera apenas classes usadas:
- Build mais rápido
- Preview mais rápido
- Suporta valores arbitrários: `w-[137px]`

## Acessibilidade

Tailwind facilita a11y:

```tsx
{/* Focus visible para navegação por teclado */}
<button className="focus:outline-none focus-visible:ring-2">

{/* Screen reader only */}
<span className="sr-only">Fechar modal</span>

{/* Tamanhos touch-friendly (min 44x44px) */}
<button className="min-w-[44px] min-h-[44px]">
```

## Plugins Úteis

### Futuros plugins a considerar:
```javascript
// tailwind.config.ts
plugins: [
  require('@tailwindcss/forms'),      // Estilos para forms
  require('@tailwindcss/typography'), // Prosa (artigos)
  require('@tailwindcss/aspect-ratio'), // Aspect ratios
]
```

## Alternativas Consideradas

| Solução | Prós | Contras | Decisão |
|---------|------|---------|---------|
| Tailwind CSS | Rápido, consistente, performance | HTML "sujo" | ✅ Escolhido |
| CSS Modules | Scoped, simples | Naming, menos opinativo | ❌ Rejeitado |
| Styled Components | Type-safe, dinâmico | Runtime overhead, RSC issues | ❌ Rejeitado |
| Emotion | Similar a SC | Mesmos problemas | ❌ Rejeitado |
| Sass/SCSS | Poderoso, familiar | Naming, sem design tokens | ❌ Rejeitado |

## Integrações

### Com Shadcn/ui (Planejado):
Tailwind é base do Shadcn/ui:
```bash
npx shadcn-ui@latest init
npx shadcn-ui@latest add button
```

### Com Next.js:
Zero config, funciona automaticamente:
```bash
npx create-next-app@latest --tailwind
```

## Referências
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Tailwind CSS Best Practices](https://tailwindcss.com/docs/reusing-styles)
- [Tailwind CSS with Next.js](https://tailwindcss.com/docs/guides/nextjs)
- [Tailwind UI Components](https://tailwindui.com/)

## Notas de Implementação
- Versão: Tailwind CSS 3.4+
- JIT Mode: Enabled (default)
- PostCSS: Configurado automaticamente
- VS Code Extension: Tailwind CSS IntelliSense
- Prettier Plugin: prettier-plugin-tailwindcss (ordena classes)

