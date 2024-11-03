import * as React from "react"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { MessageSquare } from "lucide-react"
import { cn } from "@/lib/utils"
import { useRouter } from "next/navigation"
import { createClient } from "@supabase/supabase-js"
import { Progress } from "@/components/ui/progress"

// Initialize Supabase client
const supabaseUrl = "https://hpqjqscppcxkorulngck.supabase.co"
const supabaseKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhwcWpxc2NwcGN4a29ydWxuZ2NrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzA1MTI1MjMsImV4cCI6MjA0NjA4ODUyM30.mQyDxrnj49FcO839wDlIVbSspTXJ2NlienlfeWSq6Lw"
const supabase = createClient(supabaseUrl, supabaseKey)

interface Test {
  test_id: string
  created_at: string
  task: string
  task_type: object
  goal: string
  persona: string
  persona_type: object
  conversation: { role: string; content: string }[]
  repetitiveness_metric: number
  helpfulness_metric: number
  num_exchanges: number
  goal_completion_accuracy: number
  goal_completion_reasoning: string
  status: string
}

export default function ViewChatHistory() {
  const [chatHistory, setChatHistory] = React.useState<{ role: string; content: string }[]>([])
  const [testDetails, setTestDetails] = React.useState<Test | null>(null)
  const [pastConversations, setPastConversations] = React.useState<{ id: string; title: string; date: string }[]>([])
  const router = useRouter()
  const chatContainerRef = React.useRef<HTMLDivElement>(null)

  React.useEffect(() => {
    const fetchChatHistory = async () => {
      const searchParams = new URLSearchParams(window.location.search)
      const testId = searchParams.get("test_id")

      if (testId) {
        const { data: testData, error: testError } = await supabase
          .from("LLMQA")
          .select(
            "test_id, created_at, task, task_type, goal, persona, persona_type, conversation, repetitiveness_metric, helpfulness_metric, num_exchanges, goal_completion_accuracy, goal_completion_reasoning, status"
          )
          .eq("test_id", testId)
          .single()

        if (testError) {
          console.error("Error fetching test details:", testError)
        } else {
          setTestDetails(testData as Test)
          try {
            const conversation = JSON.parse(testData.conversation)
            setChatHistory(Array.isArray(conversation) ? conversation : [])
          } catch (error) {
            console.error("Error parsing conversation:", error)
            setChatHistory([])
          }
        }
      }
    }

    fetchChatHistory()
  }, [])

  React.useEffect(() => {
    const fetchPastConversations = async () => {
      const { data, error } = await supabase
        .from("LLMQA")
        .select("test_id, created_at, task")

      if (error) {
        console.error("Error fetching past conversations:", error)
      } else {
        const formattedConversations = data.map((test: any) => ({
          id: test.test_id,
          title: test.task.split(" ").slice(0, 4).join(" ") + (test.task.split(" ").length > 4 ? "..." : ""),
          date: new Date(test.created_at).toLocaleDateString(),
        }))
        setPastConversations(formattedConversations)
      }
    }

    fetchPastConversations()
  }, [])

  React.useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight
    }
  }, [chatHistory])

  return (
    <div className="flex h-full">
      <aside className="w-64 bg-background border-r p-0">
        <ScrollArea className="h-[calc(100vh-120px)]">
          <ul className="space-y-2">
            {pastConversations.map((conversation) => (
              <li key={conversation.id} className="w-full">
                <Button
                  variant="ghost"
                  className={`w-full justify-start text-left flex-col items-start p-3 ${testDetails?.test_id === conversation.id ? "bg-muted" : ""}`}
                  onClick={() => window.location.href = `/view-chat-history?test_id=${conversation.id}`}
                >
                  <div className="flex flex-col items-start w-full">
                    <span className="text-sm font-medium break-words whitespace-normal overflow-hidden">
                      {conversation.title}
                    </span>
                    <span className="text-xs text-muted-foreground">
                      {conversation.date}
                    </span>
                  </div>
                </Button>
              </li>
            ))}
          </ul>
        </ScrollArea>
      </aside>
      <div className="flex-1 flex flex-col overflow-hidden">
        <header className="flex items-center p-4 border-b">
          <h1 className="text-xl font-semibold ml-4">Chat History</h1>
        </header>
        <div className="flex-1 overflow-auto p-4">
          {testDetails && (
            <Card className="mb-4">
              <CardHeader>
                <CardTitle>Test Details</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <div>
                    <span className="font-semibold">Task:</span> {testDetails.task}
                  </div>
                  <div>
                    <span className="font-semibold">Goal:</span> {testDetails.goal}
                  </div>
                  <div>
                    <span className="font-semibold">Completion Accuracy:</span>
                    <div className="flex items-center justify-center mt-2">
                      <span className="mr-2">1</span>
                      <div className="flex-1 max-w-[50%]">
                        <Progress value={testDetails.goal_completion_accuracy * 10} />
                      </div>
                      <span className="ml-2">10</span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          <Card>
            <CardHeader>
              <CardTitle>Chat History</CardTitle>
            </CardHeader>
            <CardContent>
              <ScrollArea className="h-[calc(100vh-400px)] pr-4" ref={chatContainerRef}>
                <div className="space-y-4">
                  {chatHistory.map((message, index) => (
                    <div
                      key={index}
                      className={`flex ${
                        message.role === "user" ? "justify-end" : "justify-start"
                      }`}
                    >
                      <div
                        className={`flex max-w-[80%] ${
                          message.role === "user"
                            ? "flex-row-reverse"
                            : "flex-row"
                        }`}
                      >
                        <Avatar className={message.role === "user" ? "ml-2" : "mr-2"}>
                          <AvatarImage
                            src="/avatar-placeholder.png" alt={message.role}
                          />
                          <AvatarFallback>
                            {message.role === "user" ? "U" : "A"}
                          </AvatarFallback>
                        </Avatar>
                        <div
                          className={`rounded-lg p-3 ${
                            message.role === "user"
                              ? "bg-primary text-primary-foreground"
                              : "bg-muted"
                          }`}
                        >
                          <p className="text-sm whitespace-pre-wrap">
                            {message.content}
                          </p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </ScrollArea>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
