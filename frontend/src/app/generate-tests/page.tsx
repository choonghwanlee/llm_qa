"use client";

import { useState } from "react";
import TestCreator from "../../components/ui/test-creator";
import TestList from "../../components/ui/test-list";
import { motion } from "framer-motion";
import Layout from "../../components/Layout";
import { usePathname } from "next/navigation";

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
  const pathname = usePathname();

  return (
    <Layout>
        <motion.div
      key={pathname} // Use pathname to uniquely identify the page
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.5 }}
      className="flex flex-col min-h-screen bg-background text-foreground"
    >
    <div className="container mx-auto p-4 space-y-8">
      <TestCreator onTestCreated={handleTestCreated} />
      <TestList tests={tests} />
    </div>
    </motion.div>
    </Layout>
  );
}
