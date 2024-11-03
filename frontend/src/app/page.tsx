"use client";

import * as React from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ArrowRight, BarChart, Zap, RefreshCw } from "lucide-react"
import { Settings, User } from "lucide-react";
import { motion } from "framer-motion";
import { usePathname } from "next/navigation";

import Link from "next/link"

export default function LandingPage() {
  const pathname = usePathname(); 
  return (
    
    <div className="flex flex-col min-h-screen bg-background text-foreground">
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
      <motion.div
      key={pathname} // Use pathname to uniquely identify the page
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.5 }}
      className="flex flex-col min-h-screen bg-background text-foreground"
    >
      <main className="flex-grow">
        <section className="py-20 text-center">
          <div className="container mx-auto px-4">
            <h2 className="text-4xl font-bold mb-4">Transforming Chatbots and Voice Agents with Intelligent Evaluation</h2>
            <p className="text-xl mb-8 max-w-3xl mx-auto">
              Optimize your conversational agents to deliver exceptional customer experiences. Evalon's LLM evaluation framework helps you assess and improve your chatbots and voice agents for optimal performance.
            </p>
            <Link href="/dashboard" passHref>
              <Button size="lg">
                Get Started Now
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </Link>
          </div>
        </section>

        <section className="py-20 bg-muted">
          <div className="container mx-auto px-4">
            <h3 className="text-3xl font-bold mb-12 text-center">Key Value Propositions</h3>
            <div className="grid md:grid-cols-3 gap-8">
              <Card>
                <CardHeader>
                  <CardTitle>Assess</CardTitle>
                </CardHeader>
                <CardContent>
                  <p>Evaluate your AI agents with real-time performance insights.</p>
                </CardContent>
              </Card>
              <Card>
                <CardHeader>
                  <CardTitle>Optimize</CardTitle>
                </CardHeader>
                <CardContent>
                  <p>Use Evalon's feedback to fine-tune interactions, reducing repetitive and unhelpful responses.</p>
                </CardContent>
              </Card>
              <Card>
                <CardHeader>
                  <CardTitle>Thrive</CardTitle>
                </CardHeader>
                <CardContent>
                  <p>Improve user satisfaction, reduce costs, and differentiate your business from competitors.</p>
                </CardContent>
              </Card>
            </div>
          </div>
        </section>

        <section className="py-20">
          <div className="container mx-auto px-4">
            <h3 className="text-3xl font-bold mb-12 text-center">How It Works</h3>
            <div className="grid md:grid-cols-3 gap-8">
              <div className="text-center">
                <div className="mb-4 inline-block p-4 bg-muted rounded-full">
                  <Zap className="h-8 w-8" />
                </div>
                <h4 className="text-xl font-semibold mb-2">Integration</h4>
                <p>Seamlessly integrate your chatbots or voice agents with Evalon.</p>
              </div>
              <div className="text-center">
                <div className="mb-4 inline-block p-4 bg-muted rounded-full">
                  <BarChart className="h-8 w-8" />
                </div>
                <h4 className="text-xl font-semibold mb-2">Evaluation</h4>
                <p>Get real-time quantitative and qualitative evaluation metrics.</p>
              </div>
              <div className="text-center">
                <div className="mb-4 inline-block p-4 bg-muted rounded-full">
                  <RefreshCw className="h-8 w-8" />
                </div>
                <h4 className="text-xl font-semibold mb-2">Insights & Action</h4>
                <p>Receive actionable insights and recommendations to improve performance.</p>
              </div>
            </div>
          </div>
        </section>

        <section className="py-20 bg-muted text-center">
          <div className="container mx-auto px-4">
            <h3 className="text-3xl font-bold mb-8">Ready to elevate your AI-driven interactions?</h3>
            <Button size="lg">
              Schedule a Demo
              <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          </div>
        </section>
      </main>

      <footer className="border-t py-8">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <h4 className="font-semibold mb-4">About</h4>
              <ul className="space-y-2">
                <li><a href="#" className="hover:underline">Our Story</a></li>
                <li><a href="#" className="hover:underline">Team</a></li>
                <li><a href="#" className="hover:underline">Careers</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Product</h4>
              <ul className="space-y-2">
                <li><a href="#" className="hover:underline">Features</a></li>
                <li><a href="#" className="hover:underline">Pricing</a></li>
                <li><a href="#" className="hover:underline">FAQ</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Resources</h4>
              <ul className="space-y-2">
                <li><a href="#" className="hover:underline">Blog</a></li>
                <li><a href="#" className="hover:underline">Documentation</a></li>
                <li><a href="#" className="hover:underline">Support</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Legal</h4>
              <ul className="space-y-2">
                <li><a href="#" className="hover:underline">Privacy Policy</a></li>
                <li><a href="#" className="hover:underline">Terms of Service</a></li>
                <li><a href="#" className="hover:underline">Cookie Policy</a></li>
              </ul>
            </div>
          </div>
          <div className="mt-8 text-center text-sm text-muted-foreground">
            © {new Date().getFullYear()} Evalon. All rights reserved.
          </div>
        </div>
      </footer>
      </motion.div>
    </div>
   
  )
}