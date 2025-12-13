"use client"

import { X } from "lucide-react"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

interface Tab {
  id: string
  label: string
  path: string
}

interface TabBarProps {
  tabs: Tab[]
  activeTab: string | null
  onTabClick: (tab: Tab) => void
  onTabClose: (id: string) => void
}

export function TabBar({ tabs, activeTab, onTabClick, onTabClose }: TabBarProps) {
  return (
    <div className="h-10 border-b bg-muted/50 flex items-center gap-1 px-2 overflow-x-auto">
      {tabs.map((tab) => (
        <div
          key={tab.id}
          className={cn(
            "flex items-center gap-2 px-3 py-1.5 rounded-t-md cursor-pointer transition-colors",
            activeTab === tab.id
              ? "bg-background border-t border-l border-r"
              : "hover:bg-muted"
          )}
          onClick={() => onTabClick(tab)}
        >
          <span className="text-sm whitespace-nowrap">{tab.label}</span>
          <Button
            variant="ghost"
            size="icon"
            className="h-4 w-4"
            onClick={(e) => {
              e.stopPropagation()
              onTabClose(tab.id)
            }}
          >
            <X className="h-3 w-3" />
          </Button>
        </div>
      ))}
    </div>
  )
}
