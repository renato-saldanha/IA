import Link from 'next/link'
import { MessageSquare, FileText, HelpCircle, Ticket as TicketIcon } from 'lucide-react'

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-primary-600">
                SaaS Suporte
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <Link
                href="/auth/login"
                className="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium"
              >
                Entrar
              </Link>
              <Link
                href="/auth/register"
                className="bg-primary-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-primary-700"
              >
                Criar Conta
              </Link>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-16">
          <h2 className="text-5xl font-extrabold text-gray-900 mb-4">
            Suporte ao Cliente
            <span className="text-primary-600"> Completo</span>
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Sistema profissional de help desk com chat ao vivo, base de conhecimento
            e portal de autoatendimento. Tudo em uma só plataforma.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8 mb-16">
          <div className="bg-white rounded-lg shadow-lg p-8 hover:shadow-xl transition-shadow">
            <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
              <TicketIcon className="w-6 h-6 text-primary-600" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">
              Sistema de Tickets
            </h3>
            <p className="text-gray-600 mb-4">
              Gerencie todas as solicitações de suporte em um só lugar. 
              Organize, priorize e resolva tickets com eficiência.
            </p>
            <ul className="space-y-2 text-sm text-gray-600">
              <li>✓ Priorização automática</li>
              <li>✓ Atribuição de agentes</li>
              <li>✓ Histórico completo</li>
              <li>✓ Status em tempo real</li>
            </ul>
          </div>

          <div className="bg-white rounded-lg shadow-lg p-8 hover:shadow-xl transition-shadow">
            <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
              <MessageSquare className="w-6 h-6 text-green-600" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">
              Chat ao Vivo
            </h3>
            <p className="text-gray-600 mb-4">
              Atenda seus clientes em tempo real com nossa ferramenta de chat
              ao vivo integrada e intuitiva.
            </p>
            <ul className="space-y-2 text-sm text-gray-600">
              <li>✓ Resposta em tempo real</li>
              <li>✓ Fila de atendimento</li>
              <li>✓ Histórico de conversas</li>
              <li>✓ Avaliação de atendimento</li>
            </ul>
          </div>

          <div className="bg-white rounded-lg shadow-lg p-8 hover:shadow-xl transition-shadow">
            <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
              <HelpCircle className="w-6 h-6 text-purple-600" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">
              Base de Conhecimento
            </h3>
            <p className="text-gray-600 mb-4">
              Portal de autoatendimento com artigos, FAQs e tutoriais para
              que seus clientes resolvam dúvidas sozinhos.
            </p>
            <ul className="space-y-2 text-sm text-gray-600">
              <li>✓ Artigos organizados</li>
              <li>✓ Busca inteligente</li>
              <li>✓ Categorização</li>
              <li>✓ Métricas de utilidade</li>
            </ul>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-lg p-12 text-center">
          <h3 className="text-3xl font-bold text-gray-900 mb-4">
            Pronto para começar?
          </h3>
          <p className="text-lg text-gray-600 mb-8">
            Crie sua conta gratuitamente e comece a oferecer o melhor suporte
            aos seus clientes.
          </p>
          <div className="flex justify-center space-x-4">
            <Link
              href="/auth/register"
              className="bg-primary-600 text-white px-8 py-3 rounded-lg text-lg font-medium hover:bg-primary-700 transition-colors"
            >
              Criar Conta Grátis
            </Link>
            <Link
              href="/knowledge"
              className="bg-gray-200 text-gray-700 px-8 py-3 rounded-lg text-lg font-medium hover:bg-gray-300 transition-colors"
            >
              Ver Base de Conhecimento
            </Link>
          </div>
        </div>
      </main>

      <footer className="bg-white border-t mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <p className="text-center text-gray-500">
            © 2024 SaaS de Suporte ao Cliente. Todos os direitos reservados.
          </p>
        </div>
      </footer>
    </div>
  )
}

