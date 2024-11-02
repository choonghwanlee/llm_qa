"use client";

import { useState } from "react"
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
import { Settings, User, ChevronDown } from "lucide-react"
import { StarFilledIcon, StarIcon } from "@radix-ui/react-icons"
import {
  DropdownMenu,
  DropdownMenuCheckboxItem,
  DropdownMenuContent,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

// Mock data
const initialTests = [
  { id: 1, task: "Scheduling", goal: "Book appointment", persona: "Young Adult", metric1: 8.5, metric2: 7.9 },
  { id: 2, task: "Support", goal: "Technical help", persona: "Confused Adult", metric1: 3.2, metric2: 4.1 },
  { id: 3, task: "Inquiry", goal: "Product information", persona: "Angry Uncle", metric1: 6.7, metric2: 5.8 },
  { id: 4, task: "Complaint", goal: "Resolve issue", persona: "Chinese Grandma", metric1: 4.5, metric2: 3.9 },
]

export default function Component() {
  const [tests, setTests] = useState(initialTests)
  type FilterKeys = 'youngAdult' | 'confusedAdult' | 'angryUncle' | 'chineseGrandma';

  const [filters, setFilters] = useState({
    youngAdult: true,
    confusedAdult: true,
    angryUncle: true,
    chineseGrandma: true,
  })

  const updateFilters = (key: FilterKeys) => {
    setFilters(prev => ({ ...prev, [key]: !prev[key] }))
  }

  const applyFilters = () => {
    const filteredTests = initialTests.filter(test => 
      (filters.youngAdult && test.persona === "Young Adult") ||
      (filters.confusedAdult && test.persona === "Confused Adult") ||
      (filters.angryUncle && test.persona === "Angry Uncle") ||
      (filters.chineseGrandma && test.persona === "Chinese Grandma")
    )
    setTests(filteredTests)
  }

  // Calculate summary statistics
  const taskFulfillment = tests.reduce((sum, test) => sum + test.metric2, 0) / tests.length

  return (
    <div className="min-h-screen bg-background">
      {/* Top Navigation */}
      <header className="border-b">
        <div className="flex h-16 items-center px-4">
          <div className="flex items-center">
            <img src="/logo.svg" alt="Logo" className="h-10 w-10" />
            <span className="ml-2 text-xl font-bold">Evalon</span>
          </div>
          <nav className="ml-6 flex items-center space-x-4">
            <Button variant="default">Dashboard</Button>
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="outline">
                  Filter Options <ChevronDown className="ml-2 h-4 w-4" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent className="w-56">
                <DropdownMenuLabel>Filter by Persona</DropdownMenuLabel>
                <DropdownMenuSeparator />
                <DropdownMenuCheckboxItem
                  checked={filters.youngAdult}
                  onCheckedChange={() => updateFilters("youngAdult")}
                >
                  Young Adult
                </DropdownMenuCheckboxItem>
                <DropdownMenuCheckboxItem
                  checked={filters.confusedAdult}
                  onCheckedChange={() => updateFilters("confusedAdult")}
                >
                  Confused Adult
                </DropdownMenuCheckboxItem>
                <DropdownMenuCheckboxItem
                  checked={filters.angryUncle}
                  onCheckedChange={() => updateFilters("angryUncle")}
                >
                  Angry Uncle
                </DropdownMenuCheckboxItem>
                <DropdownMenuCheckboxItem
                  checked={filters.chineseGrandma}
                  onCheckedChange={() => updateFilters("chineseGrandma")}
                >
                  Chinese Grandma
                </DropdownMenuCheckboxItem>
                <DropdownMenuSeparator />
                <Button onClick={applyFilters} className="w-full">Apply Filters</Button>
              </DropdownMenuContent>
            </DropdownMenu>
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
        <aside className="w-64 border-r bg-muted/40 p-4">
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
        <main className="flex-1 p-6">
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
                          <Progress value={taskFulfillment} className="h-32 w-32" />
                          <span className="ml-4 text-2xl font-bold">{taskFulfillment.toFixed(1)}%</span>
                        </div>
                        <div className="flex flex-col items-center">
                          <CardTitle>Average Rating</CardTitle>
                          <Progress value={7.5} className="h-6 w-48 mt-2" />
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
                      <div className="space-y-2">
                        <div className="flex items-center justify-between">
                          <span>Helpfulness</span>
                          <div className="flex">
                            {[1, 2, 3, 4, 5].map((i) => (
                              i <= 3 ? 
                              <StarFilledIcon key={i} className="h-5 w-5 text-yellow-500" /> :
                              <StarIcon key={i} className="h-5 w-5 text-muted" />
                            ))}
                          </div>
                        </div>
                        <div className="flex items-center justify-between">
                          <span>Repetitiveness</span>
                          <div className="flex">
                            {[1, 2, 3, 4, 5].map((i) => (
                              i <= 2 ? 
                              <StarFilledIcon key={i} className="h-5 w-5 text-yellow-500" /> :
                              <StarIcon key={i} className="h-5 w-5 text-muted" />
                            ))}
                          </div>
                        </div>
                        <div className="flex items-center justify-between">
                          <span>Safety</span>
                          <div className="flex">
                            {[1, 2, 3, 4, 5].map((i) => (
                              i <= 4 ? 
                              <StarFilledIcon key={i} className="h-5 w-5 text-yellow-500" /> :
                              <StarIcon key={i} className="h-5 w-5 text-muted" />
                            ))}
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>

                  {/* Bottom Left - Personas */}
                  <Card>
                    <CardHeader>
                      <CardTitle>Personas</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="grid gap-4 md:grid-cols-2">
                        <Card className="bg-green-100">
                          <CardHeader>
                            <CardTitle>Best Performing Personas</CardTitle>
                          </CardHeader>
                          <CardContent>
                            <div className="space-y-1">
                              <div className="flex justify-between">
                                <span>Angry Uncle</span>
                              </div>
                              <div className="flex justify-between">
                                <span>Young Adult</span>
                              </div>
                              <div className="flex justify-between">
                                <span>Chinese Grandma</span>
                              </div>
                            </div>
                          </CardContent>
                        </Card>
                        <Card className="bg-red-100">
                          <CardHeader>
                            <CardTitle>Poorest Performing Personas</CardTitle>
                          </CardHeader>
                          <CardContent>
                            <div className="space-y-1">
                              <div className="flex justify-between">
                                <span>Confused Adult</span>
                              </div>
                              <div className="flex justify-between">
                                <span>Soul Gamer</span>
                              </div>
                            </div>
                          </CardContent>
                        </Card>
                      </div>
                    </CardContent>
                  </Card>

                  {/* Bottom Right - Task Categories */}
                  <Card>
                    <CardHeader>
                      <CardTitle>Task Categories</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="grid gap-4 md:grid-cols-2">
                        <Card className="bg-green-100">
                          <CardHeader>
                            <CardTitle>Top Performing Categories</CardTitle>
                          </CardHeader>
                          <CardContent>
                            <div className="space-y-1">
                              <div className="flex justify-between">
                                <span>Scheduling</span>
                              </div>
                              <div className="flex justify-between">
                                <span>Answering Questions</span>
                              </div>
                            </div>
                          </CardContent>
                        </Card>
                        <Card className="bg-red-100">
                          <CardHeader>
                            <CardTitle>Poor Performing Categories</CardTitle>
                          </CardHeader>
                          <CardContent>
                            <div className="space-y-1">
                              <div className="flex justify-between">
                                <span>Technical Help</span>
                              </div>
                              <div className="flex justify-between">
                                <span>Complaint Resolution</span>
                              </div>
                            </div>
                          </CardContent>
                        </Card>
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
                      <TableHead>Task</TableHead>
                      <TableHead>Goal</TableHead>
                      <TableHead>Persona</TableHead>
                      <TableHead>Metric 1</TableHead>
                      <TableHead>Metric 2</TableHead>
                      <TableHead>View Chat</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {tests.map((test) => (
                      <TableRow key={test.id}>
                        <TableCell>{test.task}</TableCell>
                        <TableCell>{test.goal}</TableCell>
                        <TableCell>{test.persona}</TableCell>
                        <TableCell>{test.metric1.toFixed(1)}</TableCell>
                        <TableCell>{test.metric2.toFixed(1)}</TableCell>
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
