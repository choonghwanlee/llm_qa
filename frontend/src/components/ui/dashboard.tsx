"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { createClient } from "@supabase/supabase-js";

// Initialize Supabase client
const supabaseUrl = "https://hpqjqscppcxkorulngck.supabase.co";
const supabaseKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhwcWpxc2NwcGN4a29ydWxuZ2NrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzA1MTI1MjMsImV4cCI6MjA0NjA4ODUyM30.mQyDxrnj49FcO839wDlIVbSspTXJ2NlienlfeWSq6Lw";
const supabase = createClient(supabaseUrl, supabaseKey);

interface Test {
  test_id: string;
  created_at: string;
  task: string;
  goal: string;
  persona: string;
  helpfulness_metric: number;
  repetitiveness_metric: number;
  goal_completion_accuracy: number;
}

export default function Dashboard() {
  const [tests, setTests] = useState<Test[]>([]);
  const router = useRouter();

  useEffect(() => {
    const fetchTests = async () => {
      const { data, error } = await supabase
        .from('LLMQA')
        .select('test_id, created_at, task, goal, persona, helpfulness_metric, repetitiveness_metric, goal_completion_accuracy');

      if (error) {
        console.error("Error fetching tests:", error);
      } else {
        const filteredData = data.filter((test: any) => test.created_at && test.task && test.goal && test.persona && test.helpfulness_metric !== null && test.repetitiveness_metric !== null && test.goal_completion_accuracy !== null) as Test[];
        setTests(filteredData);
      }
    };

    fetchTests();
  }, []);

  // Calculate summary statistics
  const totalTests = tests.length;
  const fulfilledTests = tests.filter(test => test.goal_completion_accuracy > 7).length;
  const taskFulfillment = totalTests > 0 ? (fulfilledTests / totalTests) * 100 : 0;
  const averageRating = totalTests > 0 ? (tests.reduce((sum, test) => sum + (test.goal_completion_accuracy || 0), 0) / totalTests) * 10 : 0;
  const averageHelpfulness = totalTests > 0 ? (tests.reduce((sum, test) => sum + (test.helpfulness_metric || 0), 0) / totalTests) * 10 : 0;
  const averageRepetitiveness = totalTests > 0 ? (tests.reduce((sum, test) => sum + (test.repetitiveness_metric || 0), 0) / totalTests) * 10 : 0;

  return (
    <div className="min-h-screen bg-white text-black">
      <div className="flex">
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

            {/* Personas and Task Categories */}
            <div className="grid gap-6 md:grid-cols-2">
              {/* Personas Card */}
              <Card>
                <CardHeader>
                  <CardTitle>Personas</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-green-100 p-4 rounded-lg">
                      <h3 className="font-bold">Best</h3>
                      <ul className="mt-2 space-y-1">
                        <li>Angry Uncle <span className="float-right">9.9</span></li>
                        <li>Young Adult <span className="float-right">8.5</span></li>
                        <li>Chinese Grandma <span className="float-right">7.3</span></li>
                      </ul>
                    </div>
                    <div className="bg-red-100 p-4 rounded-lg">
                      <h3 className="font-bold">Worst</h3>
                      <ul className="mt-2 space-y-1">
                        <li>Confused Adult <span className="float-right">1.3</span></li>
                        <li>Soul Gamer <span className="float-right">0.3</span></li>
                      </ul>
                    </div>
                  </div>
                </CardContent>
              </Card>
              {/* Task Categories Card */}
              <Card>
                <CardHeader>
                  <CardTitle>Task Categories</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-green-100 p-4 rounded-lg">
                      <h3 className="font-bold">Best</h3>
                      <ul className="mt-2 space-y-1">
                        <li>Scheduling <span className="float-right">8.3</span></li>
                        <li>Answering Questions <span className="float-right">7.5</span></li>
                      </ul>
                    </div>
                    <div className="bg-red-100 p-4 rounded-lg">
                      <h3 className="font-bold">Worst</h3>
                      <ul className="mt-2 space-y-1">
                        <li>Technical Help <span className="float-right">3.2</span></li>
                        <li>Complaint Resolution <span className="float-right">3.9</span></li>
                      </ul>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* All Tests Table */}
            <Card>
              <CardHeader>
                <CardTitle>All Tests</CardTitle>
              </CardHeader>
              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead className="w-48  ">Created At</TableHead>
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
                        <TableCell>{new Date(test.created_at).toLocaleString('en-US', { hour: 'numeric', hour12: true, day: 'numeric', month: 'short', year: 'numeric' })}</TableCell>
                        <TableCell>{test.task}</TableCell>
                        <TableCell className="whitespace-normal">{test.goal}</TableCell>
                        <TableCell>{test.persona}</TableCell>
                        <TableCell>{test.helpfulness_metric.toFixed(1)}</TableCell>
                        <TableCell>{test.repetitiveness_metric.toFixed(1)}</TableCell>
                        <TableCell>{test.goal_completion_accuracy.toFixed(1)}</TableCell>
                        <TableCell>
                          <Button variant="ghost" size="sm" onClick={() => router.push(`/view-chat-history?test_id=${test.test_id}`)}>View</Button>
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
  );
}
