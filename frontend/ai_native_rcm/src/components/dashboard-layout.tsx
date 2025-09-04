import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Home, User, FileText, Settings, Menu } from "lucide-react"

interface DashboardLayoutProps {
  children: React.ReactNode
}

export function DashboardLayout({ children }: DashboardLayoutProps) {
  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      <div className="w-64 bg-white shadow-lg">
        <div className="p-6">
          <h2 className="text-xl font-semibold text-gray-800">Dashboard</h2>
        </div>
        
        <nav className="mt-6">
          <div className="px-4 space-y-2">
            <Link href="/dashboard">
              <Button 
                variant="ghost" 
                className="w-full justify-start text-left"
              >
                <Home className="mr-3 h-4 w-4" />
                Overview
              </Button>
            </Link>
            
            <Link href="/dashboard/profile">
              <Button 
                variant="ghost" 
                className="w-full justify-start text-left"
              >
                <User className="mr-3 h-4 w-4" />
                Profile
              </Button>
            </Link>

            <Link href="/dashboard/claims">
              <Button 
                variant="ghost" 
                className="w-full justify-start text-left"
              >
                <FileText className="mr-3 h-4 w-4" />
                Claims
              </Button>
            </Link>
          </div>
        </nav>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-auto">
        <div className="p-8">
          {children}
        </div>
      </div>
    </div>
  )
}