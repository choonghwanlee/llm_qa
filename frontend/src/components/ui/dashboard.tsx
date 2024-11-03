"use client";

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Button } from "@/components/ui/button"
import { Settings, User } from "lucide-react"
import { createClient } from "@supabase/supabase-js"

// Initialize Supabase client
const supabaseUrl = "https://hpqjqscppcxkorulngck.supabase.co"
const supabaseKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhwcWpxc2NwcGN4a29ydWxuZ2NrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzA1MTI1MjMsImV4cCI6MjA0NjA4ODUyM30.mQyDxrnj49FcO839wDlIVbSspTXJ2NlienlfeWSq6Lw"
const supabase = createClient(supabaseUrl, supabaseKey)

interface Test {
  test_id: number;
  created_at: string;
  task: string;
  goal: string;
  persona: string;
  helpfulness_metric: number;
  repetitiveness_metric: number;
  goal_completion_accuracy: number;
}

export default function Component() {
  const [tests, setTests] = useState<Test[]>([])

  useEffect(() => {
    const fetchTests = async () => {
      const { data, error } = await supabase
        .from('LLMQA')
        .select('test_id, created_at, task, goal, persona, helpfulness_metric, repetitiveness_metric, goal_completion_accuracy')

      if (error) {
        console.error("Error fetching tests:", error)
      } else {
        const filteredData = data.filter((test: any) => test.created_at && test.task && test.goal && test.persona && test.helpfulness_metric !== null && test.repetitiveness_metric !== null && test.goal_completion_accuracy !== null) as Test[];
        setTests(filteredData)
      }
    }

    fetchTests()
  }, [])

  // Calculate summary statistics
  const totalTests = tests.length
  const fulfilledTests = tests.filter(test => test.goal_completion_accuracy > 7).length
  const taskFulfillment = totalTests > 0 ? (fulfilledTests / totalTests) * 100 : 0
  const averageRating = totalTests > 0 ? (tests.reduce((sum, test) => sum + (test.goal_completion_accuracy || 0), 0) / totalTests) * 10 : 0;
  const averageHelpfulness = totalTests > 0 ? (tests.reduce((sum, test) => sum + (test.helpfulness_metric || 0), 0) / totalTests) * 10 : 0;
  const averageRepetitiveness = totalTests > 0 ? (tests.reduce((sum, test) => sum + (test.repetitiveness_metric || 0), 0) / totalTests) * 10 : 0

  return (
    <div className="min-h-screen bg-white text-black">
      {/* Top Navigation */}
      <header className="border-b bg-white">
        <div className="flex h-16 items-center px-4">
          <div className="flex items-center">
            <img src="/logo.svg" alt="Logo" className="h-10 w-10" />
            <span className="ml-2 text-xl font-bold">Evalon</span>
          </div>
          <nav className="ml-6 flex items-center space-x-4">
            <Button variant="default">Dashboard</Button>
          </nav>
          <div className="ml-auto flex items-center space-x-4">
            <Button variant="ghost" size="icon">
              <Settings className="h-5 w-5" />
            </Button>
            <Button variant="ghost" size="icon">
              <User className="h-5 w-5" />
            </Button>
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Sidebar */}
        <aside className="w-64 border-r bg-white p-4">
          <nav className="space-y-2">
            <Button variant="secondary" className="w-full justify-start">
              Generate Tasks
            </Button>
            <Button variant="ghost" className="w-full justify-start">
              Run Tasks
            </Button>
            <Button variant="ghost" className="w-full justify-start">
              View Chat History
            </Button>
          </nav>
        </aside>

        {/* Main Content */}
        <main className="flex-1 p-6 bg-white">
          <div className="grid gap-6">
            {/* Agent Overview */}
            <Card>
              <CardHeader>
                <CardTitle>Agent Overview</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid gap-6 md:grid-cols-2">
                  {/* Top Left - Task Fulfillment & Average Rating */}
                  <Card>
                    <CardHeader>
                      <CardTitle>Task Fulfillment & Average Rating</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="flex items-center justify-around">
                        <div className="flex items-center">
                          <Progress value={taskFulfillment} className="h-32 w-32 rounded-full" />
                          <span className="ml-4 text-2xl font-bold">{taskFulfillment.toFixed(1)}%</span>
                        </div>
                        <div className="flex flex-col items-center">
                          <CardTitle>Average Rating</CardTitle>
                          <Progress value={averageRating} className="h-4 w-full mt-2 rounded-lg" />
                          <div className="flex items-center justify-between w-full mt-1">
                            <span>1</span>
                            <span>10</span>
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                  {/* Top Right - Qualitative Breakdown */}
                  <Card>
                    <CardHeader>
                      <CardTitle>Qualitative Breakdown</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-4 p-4 rounded-lg">
                        <div className="flex flex-col items-center">
                          <CardTitle>Helpfulness</CardTitle>
                          <Progress value={averageHelpfulness} className="h-4 w-full mt-2 rounded-lg" />
                          <div className="flex items-center justify-between w-full mt-1">
                            <span>1</span>
                            <span>10</span>
                          </div>
                        </div>
                        <div className="flex flex-col items-center">
                          <CardTitle>Repetitiveness</CardTitle>
                          <Progress value={averageRepetitiveness} className="h-4 w-full mt-2 rounded-lg" />
                          <div className="flex items-center justify-between w-full mt-1">
                            <span>1</span>
                            <span>10</span>
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </div>
              </CardContent>
            </Card>

            {/* All Tests Table */}
            <Card>
              <CardHeader>
                <CardTitle>All Tests</CardTitle>
              </CardHeader>
              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Created At</TableHead>
                      <TableHead>Task</TableHead>
                      <TableHead>Goal</TableHead>
                      <TableHead>Persona</TableHead>
                      <TableHead>Helpfulness</TableHead>
                      <TableHead>Repetitiveness</TableHead>
                      <TableHead>Goal Completion</TableHead>
                      <TableHead>View Chat</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {tests.map((test) => (
                      <TableRow key={test.test_id}>
                        <TableCell>{test.created_at}</TableCell>
                        <TableCell>{test.task}</TableCell>
                        <TableCell>{test.goal}</TableCell>
                        <TableCell>{test.persona}</TableCell>
                        <TableCell>{test.helpfulness_metric.toFixed(1)}</TableCell>
                        <TableCell>{test.repetitiveness_metric.toFixed(1)}</TableCell>
                        <TableCell>{test.goal_completion_accuracy.toFixed(1)}</TableCell>
                        <TableCell>
                          <Button variant="ghost" size="sm">View</Button>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          </div>
        </main>
      </div>
    </div>
  )
}
