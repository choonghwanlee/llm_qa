import * as React from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function GenerateTests() {
  return (
    <div className="flex flex-col items-center min-h-screen bg-background text-foreground p-8">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>Generate Tests</CardTitle>
        </CardHeader>
        <CardContent>
          <form className="space-y-4">
            <div>
              <Label htmlFor="testName">Test Name</Label>
              <Input id="testName" placeholder="Enter test name" />
            </div>
            <div>
              <Label htmlFor="testDescription">Description</Label>
              <Input id="testDescription" placeholder="Enter test description" />
            </div>
            <Button type="submit" className="w-full">
              Generate
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
