"use client";

// Your TestList component

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
import { Badge } from "@/components/ui/badge";
import { createClient } from "@supabase/supabase-js";
import ProgressBar from "@/components/ui/ProgressBar"; // Import the ProgressBar component

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;
const supabase = createClient(supabaseUrl, supabaseAnonKey);

interface Test {
  test_id: string;
  task: string;
  goal: string;
  persona: string;
  status: "Run" | "Not Run";
}

export default function TestList() {
  const [tests, setTests] = useState<Test[]>([]);
  const [selectedTests, setSelectedTests] = useState<Test[]>([]);
  const [progress, setProgress] = useState({ completed: 0, total: 0 });
  const [isProgressBarOpen, setProgressBarOpen] = useState(false);

  const fetchTests = async () => {
    const { data, error } = await supabase
      .from("LLMQA") // Replace with your table name
      .select("test_id, task, goal, persona, status");
    if (error) {
      console.error("Error fetching tests:", error);
    } else {
      const sortedTests = data
        ? data.sort((a, b) => (a.status === "Not Run" ? -1 : 1)) // Sort "Not Run" before "Run"
        : [];
      setTests(sortedTests || []);
    }
  };

  useEffect(() => {
    fetchTests(); // Fetch tests every time the component mounts or the page is visited
  }, []); // Empty dependency array means this effect runs only once after the initial render

  const toggleTestSelection = (test: Test) => {
    setSelectedTests((prev) => {
      const isSelected = prev.some((t) => t.test_id === test.test_id);
      if (isSelected) {
        return prev.filter((t) => t.test_id !== test.test_id);
      } else {
        if (prev.length < 5) {
          return [...prev, test];
        } else {
          console.warn("Maximum of 5 tests can be selected");
          return prev;
        }
      }
    });
  };

  const runSelectedTests = async () => {
    setProgressBarOpen(true);
    setProgress({ completed: 0, total: selectedTests.length });

    await Promise.all(
      selectedTests.map(async (test) => {
        const { status, ...testData } = test;
        const response = await fetch("http://127.0.0.1:8000/runTests", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(testData),
        });
        await response.json();
        setProgress((prev) => ({
          ...prev,
          completed: prev.completed + 1,
        }));
      })
    );
  };

  return (
    <div className="space-y-4">
      <ProgressBar
        completed={progress.completed}
        total={progress.total}
        isOpen={isProgressBarOpen}
        onClose={() => setProgressBarOpen(false)} // Close the progress bar after completion
      />
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {tests.map((test, index) => (
          <Card key={test.test_id || index} className="relative">
            <CardHeader className="pb-2">
              <div className="flex items-center justify-between">
                <Checkbox
                  checked={selectedTests.some(
                    (t) => t.test_id === test.test_id
                  )}
                  onCheckedChange={() => toggleTestSelection(test)}
                />
                <Badge
                  variant={test.status === "Run" ? "success" : "destructive"}
                >
                  {test.status}
                </Badge>
              </div>
            </CardHeader>
            <CardContent>
              <CardTitle className="text-sm font-medium">
                Test ID: {test.test_id}
              </CardTitle>
              <p className="text-sm text-muted-foreground mt-1">
                Persona: {test.persona}
              </p>
              <p className="text-sm text-muted-foreground">Task: {test.task}</p>
              <p className="text-sm text-muted-foreground">Goal: {test.goal}</p>
            </CardContent>
          </Card>
        ))}
      </div>
      <div className="fixed bottom-4 right-4">
        <Button
          onClick={runSelectedTests}
          disabled={selectedTests.length === 0}
        >
          Run Selected Tests ({selectedTests.length})
        </Button>
      </div>
    </div>
  );
}
