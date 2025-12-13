"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Plus } from "lucide-react"
import api from "@/lib/api"

interface Cemetery {
  id: number
  name: string
  address: string
  city: string
  state: string
  is_active: boolean
}

export default function CemeteriesPage() {
  const [cemeteries, setCemeteries] = useState<Cemetery[]>([])

  useEffect(() => {
    const fetchCemeteries = async () => {
      try {
        const response = await api.get("/cemeteries")
        setCemeteries(response.data)
      } catch (error) {
        console.error("Error fetching cemeteries:", error)
      }
    }
    fetchCemeteries()
  }, [])

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Cemitérios</h2>
          <p className="text-muted-foreground">
            Gerencie os cemitérios cadastrados no sistema
          </p>
        </div>
        <Button>
          <Plus className="h-4 w-4 mr-2" />
          Novo Cemitério
        </Button>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {cemeteries.map((cemetery) => (
          <Card key={cemetery.id}>
            <CardHeader>
              <CardTitle>{cemetery.name}</CardTitle>
              <CardDescription>
                {cemetery.city}, {cemetery.state}
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">{cemetery.address}</p>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
