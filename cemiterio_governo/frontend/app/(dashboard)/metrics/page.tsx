"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts"
import api from "@/lib/api"

export default function MetricsPage() {
  const [data, setData] = useState<any[]>([])

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await api.get("/reports/plots-by-cemetery")
        setData(response.data.data || [])
      } catch (error) {
        console.error("Error fetching metrics:", error)
      }
    }
    fetchData()
  }, [])

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Métricas e Gráficos</h2>
        <p className="text-muted-foreground">
          Visualize métricas e gráficos do sistema
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Jazigos por Cemitério</CardTitle>
          <CardDescription>Distribuição de jazigos por cemitério</CardDescription>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="cemetery" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="total_plots" fill="#8884d8" name="Total de Jazigos" />
              <Bar dataKey="occupied" fill="#82ca9d" name="Ocupados" />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  )
}
