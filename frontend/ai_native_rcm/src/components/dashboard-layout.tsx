import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Home, User, FileText, Settings, Menu, ListChecks, ScanFace, ClipboardPlus} from "lucide-react"

interface DashboardLayoutProps {
  children: React.ReactNode
}

export function DashboardLayout({ children }: DashboardLayoutProps) {
  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      <div className="w-64 bg-white shadow-lg">
        <div className="p-6">
          <h1 className="text-4xl font-bold text-gray-800">Humaein</h1>
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
            
            <Link href="/dashboard/workflows">
              <Button 
                variant="ghost" 
                className="w-full justify-start text-left"
              >
                <FileText className="mr-3 h-4 w-4" />
                Workflow Runs
              </Button>
            </Link>

            <Link href="/dashboard/eligibility_checks">
              <Button 
                variant="ghost" 
                className="w-full justify-start text-left"
              >
                <ListChecks className="mr-3 h-4 w-4" />
                Eligibility Checks
              </Button>
            </Link>

            <Link href="/dashboard/prior_auths">
              <Button 
                variant="ghost" 
                className="w-full justify-start text-left"
              >
                <ScanFace className="mr-3 h-4 w-4" />
                Prior Auths
              </Button>
            </Link>

            <Link href="/dashboard/clinical_documents">
              <Button 
                variant="ghost" 
                className="w-full justify-start text-left"
              >
                <ClipboardPlus className="mr-3 h-4 w-4" />
                Clinical Documents
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

            <Link href="/dashboard/profile">
              <Button 
                variant="ghost" 
                className="w-full justify-start text-left"
              >
                <User className="mr-3 h-4 w-4" />
                Profile
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