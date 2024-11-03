// src/app/dashboard/page.tsx
"use client";

import GenerateTests from "@/components/ui/view-chat";
import Layout from "../../components/Layout";
import { motion } from "framer-motion";
import { usePathname } from "next/navigation";
import ViewChatHistory from "@/components/ui/view-chat";

export default function ViewChatPage() {
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
      <ViewChatHistory />
      </motion.div>
    </Layout>
    
  );
}
