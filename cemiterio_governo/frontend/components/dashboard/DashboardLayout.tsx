"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Sidebar } from "./Sidebar"
import { TabBar } from "./TabBar"
import { Button } from "@/components/ui/button"
import { LogOut, Menu } from "lucide-react"

interface Tab {
  id: string
  label: string
  path: string
}

export function DashboardLayout({ children }: { children: React.ReactNode }) {
  const router = useRouter()
  const [tabs, setTabs] = useState<Tab[]>([])
  const [activeTab, setActiveTab] = useState<string | null>(null)
  const [sidebarOpen, setSidebarOpen] = useState(true)

  const handleLogout = () => {
    localStorage.removeItem("token")
    router.push("/login")
  }

  const openTab = (id: string, label: string, path: string) => {
    const existingTab = tabs.find((tab) => tab.id === id)
    if (!existingTab) {
      setTabs([...tabs, { id, label, path }])
    }
    setActiveTab(id)
    router.push(path)
  }

  const closeTab = (id: string) => {
    const newTabs = tabs.filter((tab) => tab.id !== id)
    setTabs(newTabs)
    
    if (activeTab === id) {
      if (newTabs.length > 0) {
        const lastTab = newTabs[newTabs.length - 1]
        setActiveTab(lastTab.id)
        router.push(lastTab.path)
      } else {
        setActiveTab(null)
        router.push("/dashboard")
      }
    }
  }

  return (
    <div className="flex h-screen bg-background">
      <Sidebar 
        open={sidebarOpen} 
        onOpenChange={setSidebarOpen}
        onNavigate={openTab}
      />
      
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Bar */}
        <header className="h-16 border-b flex items-center justify-between px-4 bg-card">
          <div className="flex items-center gap-4">
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setSidebarOpen(!sidebarOpen)}
            >
              <Menu className="h-5 w-5" />
            </Button>
            <h1 className="text-xl font-semibold">
              Sistema de Gerenciamento de Cemitérios
            </h1>
          </div>
          <Button variant="ghost" onClick={handleLogout}>
            <LogOut className="h-4 w-4 mr-2" />
            Sair
          </Button>
        </header>

        {/* Tab Bar */}
        {tabs.length > 0 && (
          <TabBar
            tabs={tabs}
            activeTab={activeTab}
            onTabClick={(tab) => {
              setActiveTab(tab.id)
              router.push(tab.path)
            }}
            onTabClose={closeTab}
          />
        )}

        {/* Main Content */}
        <main className="flex-1 overflow-auto p-6">
          {children}
        </main>
      </div>
    </div>
  )
}
