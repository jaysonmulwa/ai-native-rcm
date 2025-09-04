"use client";

import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import Link from "next/link"

export default function Login() {
  const router = useRouter()

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    router.push("/home")
  }

  return (
    <main className="container mx-auto p-8">
      <Card className="max-w-md mx-auto">
        <CardHeader>
          <CardTitle>Login</CardTitle>
        </CardHeader>
        <CardContent>
          <form className="flex flex-col gap-4" onSubmit={handleSubmit}>
            <input
              type="email"
              placeholder="Email"
              className="border rounded px-3 py-2"
              required
            />
            <input
              type="password"
              placeholder="Password"
              className="border rounded px-3 py-2"
              required
            />
            <Button type="submit">Login</Button>
          </form>
          <div className="mt-4 text-sm text-center">
            Don't have an account?{" "}
            <Link href="/register" className="text-blue-600 underline">
              Register
            </Link>
          </div>
        </CardContent>
      </Card>
    </main>
  )
}