// src/app/components/Layout.tsx

"use client";

import { usePathname } from "next/navigation";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Settings, User } from "lucide-react";

const Layout = ({ children }: { children: React.ReactNode }) => {
  const pathname = usePathname();

  return (
    <div className="min-h-screen bg-white text-black">
      {/* Top Navigation */}
      <header className="border-b bg-white">
        <div className="flex h-16 items-center px-4">
          <div className="flex items-center">
            <Link href="/" passHref>
            <img src="/logo.svg" alt="Logo" className="h-16 w-16 cursor-pointer" />
          </Link>
            <Link href="/" passHref>
            <span className="ml-4 text-3xl font-bold cursor-pointer">Evalon</span>
          </Link>
          </div>
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
            <Link href="/dashboard" passHref>
              <Button
                variant="ghost"
                className={`w-full justify-start ${pathname === "/dashboard" ? "bg-gray-200" : ""}`}
              >
                Dashboard
              </Button>
            </Link>
            <Link href="/generate-tests" passHref>
              <Button
                variant="ghost"
                className={`w-full justify-start ${pathname === "/generate-tests" ? "bg-gray-200" : ""}`}
              >
                Generate & Run Tests
              </Button>
            </Link>
            <Link href="/view-chat-history" passHref>
              <Button
                variant="ghost"
                className={`w-full justify-start ${pathname === "/view-chat-history" ? "bg-gray-200" : ""}`}
              >
                View Chat History
              </Button>
            </Link>
          </nav>
        </aside>

        {/* Main Content */}
        <main className="flex-1 p-6 bg-white">{children}</main>
      </div>
    </div>
  );
};

export default Layout;
