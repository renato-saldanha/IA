"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Plus } from "lucide-react"
import api from "@/lib/api"

interface BurialPlot {
  id: number
  plot_number: string
  block: string | null
  row: string | null
  status: string
  owner_name: string | null
}

export default function BurialPlotsPage() {
  const [plots, setPlots] = useState<BurialPlot[]>([])

  useEffect(() => {
    const fetchPlots = async () => {
      try {
        const response = await api.get("/burial-plots")
        setPlots(response.data)
      } catch (error) {
        console.error("Error fetching burial plots:", error)
      }
    }
    fetchPlots()
  }, [])

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Jazigos</h2>
          <p className="text-muted-foreground">
            Gerencie os jazigos cadastrados no sistema
          </p>
        </div>
        <Button>
          <Plus className="h-4 w-4 mr-2" />
          Novo Jazigo
        </Button>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {plots.map((plot) => (
          <Card key={plot.id}>
            <CardHeader>
              <CardTitle>Jazigo {plot.plot_number}</CardTitle>
              <CardDescription>
                {plot.block && `Bloco ${plot.block}`}
                {plot.row && ` - Fileira ${plot.row}`}
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm">
                Status: <span className="font-medium">{plot.status}</span>
              </p>
              {plot.owner_name && (
                <p className="text-sm text-muted-foreground mt-2">
                  Proprietário: {plot.owner_name}
                </p>
              )}
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
