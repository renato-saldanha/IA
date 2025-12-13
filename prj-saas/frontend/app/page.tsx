import Link from "next/link";

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col">
      <header className="border-b border-gray-200">
        <div className="container mx-auto flex h-16 items-center justify-between px-4">
          <h1 className="text-2xl font-bold text-blue-600">SaaS de Suporte</h1>
          <nav className="flex gap-4">
            <Link href="/login" className="text-sm font-medium text-gray-700 hover:text-blue-600">
              Login
            </Link>
            <Link href="/register" className="text-sm font-medium text-gray-700 hover:text-blue-600">
              Registrar
            </Link>
          </nav>
        </div>
      </header>

      <main className="flex-1">
        <section className="container mx-auto px-4 py-20">
          <div className="mx-auto max-w-3xl text-center">
            <h2 className="mb-6 text-5xl font-bold tracking-tight text-gray-900">
              Transforme seu atendimento ao cliente
            </h2>
            <p className="mb-8 text-xl text-gray-600">
              Sistema completo de help desk com chat ao vivo, gerenciamento de tickets
              e base de conhecimento integrada.
            </p>
            <div className="flex justify-center gap-4">
              <Link
                href="/register"
                className="rounded-lg bg-blue-600 px-6 py-3 font-semibold text-white hover:bg-blue-700"
              >
                Começar Agora
              </Link>
              <Link
                href="/knowledge"
                className="rounded-lg border border-gray-300 bg-white px-6 py-3 font-semibold text-gray-700 hover:bg-gray-50"
              >
                Ver Base de Conhecimento
              </Link>
            </div>
          </div>
        </section>

        <section className="border-t border-gray-200 bg-gray-50 py-20">
          <div className="container mx-auto px-4">
            <h3 className="mb-12 text-center text-3xl font-bold text-gray-900">
              Recursos Principais
            </h3>
            <div className="grid gap-8 md:grid-cols-3">
              <div className="rounded-lg border border-gray-200 bg-white p-6">
                <h4 className="mb-2 text-xl font-semibold text-gray-900">Help Desk</h4>
                <p className="text-gray-600">
                  Gerencie todos os seus chamados em um só lugar com automação
                  e priorização inteligente.
                </p>
              </div>
              <div className="rounded-lg border border-gray-200 bg-white p-6">
                <h4 className="mb-2 text-xl font-semibold text-gray-900">Chat ao Vivo</h4>
                <p className="text-gray-600">
                  Atendimento em tempo real com suporte a múltiplos canais e
                  histórico completo.
                </p>
              </div>
              <div className="rounded-lg border border-gray-200 bg-white p-6">
                <h4 className="mb-2 text-xl font-semibold text-gray-900">Base de Conhecimento</h4>
                <p className="text-gray-600">
                  Portal de autoatendimento com artigos, FAQs e tutoriais para
                  seus clientes.
                </p>
              </div>
            </div>
          </div>
        </section>
      </main>

      <footer className="border-t border-gray-200 py-6">
        <div className="container mx-auto px-4 text-center text-sm text-gray-600">
          © 2024 SaaS de Suporte ao Cliente. Todos os direitos reservados.
        </div>
      </footer>
    </div>
  );
}

