"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Textarea } from "@/components/ui/textarea";
import { Loader2 } from "lucide-react";
import { createClient } from "@supabase/supabase-js";

// Initialize Supabase client
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

export default function TestCreator({
  onTestCreated,
}: {
  onTestCreated: (test: Test) => void;
}) {
  const [manualTest, setManualTest] = useState({
    task: "",
    goal: "",
    persona: "",
  });
  const [aiPrompt, setAiPrompt] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const handleManualSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const newTest = {
      ...manualTest,
    };
    const { data, error } = await supabase.from("LLMQA").insert([newTest]);
    if (error) {
      console.log("Error inserting test:", error);
    } else {
      onTestCreated(newTest);
      setManualTest({ task: "", goal: "", persona: "" });
    }
  };
  const handleAiSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      // Make a POST request to your FastAPI endpoint
      const response = await fetch("http://127.0.0.1:8000/createAITest", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ user_desc: aiPrompt }), // Send aiPrompt in the request body
      });

      if (!response.ok) {
        throw new Error("Failed to generate test");
      }

      const newTest = await response.json(); // Assuming the FastAPI returns the new test object

      onTestCreated(newTest); // Call the parent function with the new test
      setAiPrompt(""); // Clear the AI prompt input
    } catch (error) {
      console.error("Error generating test:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Create Chatbot QA Test</CardTitle>
        <CardDescription>
          Create a new test manually or using AI assistance
        </CardDescription>
      </CardHeader>
      <CardContent>
        <Tabs defaultValue="manual">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="manual">Manual Creation</TabsTrigger>
            <TabsTrigger value="ai">AI Assisted</TabsTrigger>
          </TabsList>
          <TabsContent value="manual">
            <form onSubmit={handleManualSubmit} className="space-y-4">
              <div className="grid w-full items-center gap-1.5">
                <Label htmlFor="task">Task</Label>
                <Input
                  id="task"
                  value={manualTest.task}
                  onChange={(e) =>
                    setManualTest({ ...manualTest, task: e.target.value })
                  }
                  placeholder="Enter the task"
                />
              </div>
              <div className="grid w-full items-center gap-1.5">
                <Label htmlFor="goal">Goal</Label>
                <Input
                  id="goal"
                  value={manualTest.goal}
                  onChange={(e) =>
                    setManualTest({ ...manualTest, goal: e.target.value })
                  }
                  placeholder="Enter the goal"
                />
              </div>
              <div className="grid w-full items-center gap-1.5">
                <Label htmlFor="persona">Persona</Label>
                <Input
                  id="persona"
                  value={manualTest.persona}
                  onChange={(e) =>
                    setManualTest({ ...manualTest, persona: e.target.value })
                  }
                  placeholder="Enter the persona"
                />
              </div>
              <Button type="submit" className="w-full">
                Create Manual Test
              </Button>
            </form>
          </TabsContent>
          <TabsContent value="ai">
            <form onSubmit={handleAiSubmit} className="space-y-4">
              <div className="grid w-full gap-1.5">
                <Label htmlFor="ai-prompt">AI Prompt</Label>
                <Textarea
                  id="ai-prompt"
                  placeholder="Describe the test you want to create..."
                  value={aiPrompt}
                  onChange={(e) => setAiPrompt(e.target.value)}
                />
              </div>
              <Button type="submit" className="w-full" disabled={isLoading}>
                {isLoading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Generating Test
                  </>
                ) : (
                  "Generate Test with AI"
                )}
              </Button>
            </form>
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  );
}
