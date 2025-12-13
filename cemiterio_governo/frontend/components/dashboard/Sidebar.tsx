"use client"

import { 
  LayoutDashboard, 
  Building2, 
  MapPin, 
  FileText, 
  Settings, 
  BarChart3,
  Users,
  Shield
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

interface SidebarProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  onNavigate: (id: string, label: string, path: string) => void
}

const menuItems = [
  { id: "dashboard", label: "Dashboard", icon: LayoutDashboard, path: "/dashboard" },
  { id: "cemeteries", label: "Cemitérios", icon: Building2, path: "/dashboard/cemeteries" },
  { id: "burial-plots", label: "Jazigos", icon: MapPin, path: "/dashboard/burial-plots" },
  { id: "reports", label: "Relatórios", icon: FileText, path: "/dashboard/reports" },
  { id: "metrics", label: "Métricas", icon: BarChart3, path: "/dashboard/metrics" },
  { id: "users", label: "Usuários", icon: Users, path: "/dashboard/users" },
  { id: "permissions", label: "Permissões", icon: Shield, path: "/dashboard/permissions" },
  { id: "settings", label: "Configurações", icon: Settings, path: "/dashboard/settings" },
]

export function Sidebar({ open, onOpenChange, onNavigate }: SidebarProps) {
  return (
    <aside
      className={cn(
        "bg-card border-r transition-all duration-300 flex flex-col",
        open ? "w-64" : "w-0 overflow-hidden"
      )}
    >
      <nav className="flex-1 p-4 space-y-2">
        {menuItems.map((item) => {
          const Icon = item.icon
          return (
            <Button
              key={item.id}
              variant="ghost"
              className="w-full justify-start"
              onClick={() => onNavigate(item.id, item.label, item.path)}
            >
              <Icon className="h-4 w-4 mr-2" />
              {item.label}
            </Button>
          )
        })}
      </nav>
    </aside>
  )
}
