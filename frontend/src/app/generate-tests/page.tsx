// src/app/dashboard/page.tsx
"use client";

import GenerateTests from "@/components/ui/generate-tests";
import Layout from "../../components/Layout";
import Dashboard from "../../components/ui/dashboard";
import { motion } from "framer-motion";
import { usePathname } from "next/navigation";

export default function DashboardPage() {
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
      <GenerateTests />
      </motion.div>
    </Layout>
    
  );
}
