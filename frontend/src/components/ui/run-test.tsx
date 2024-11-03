"use client";

import { useState } from "react";
import TestCreator from "./test-creator";
import TestList from "./test-list";

interface Test {
  test_id: string;
  task: string;
  goal: string;
  persona: string;
  status: "Run" | "Not Run";
}

export default function ChatbotQAPlatform() {
  const [tests, setTests] = useState<Test[]>([]);

  const handleTestCreated = (newTest: Test) => {
    setTests((prevTests) => [...prevTests, newTest]);
  };

  return (
    <div className="container mx-auto p-4 space-y-8">
      <TestCreator onTestCreated={handleTestCreated} />
      <TestList tests={tests} />
    </div>
  );
}
