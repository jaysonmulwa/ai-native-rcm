import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { DashboardLayout } from "@/components/dashboard-layout"
import { EligibilityChecksTable } from "@/components/eligibility-checks-table"

export default function EligibilityChecks() {
  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Eligibility Checks</h1>
          <p className="text-muted-foreground">
            View eligibility checks and their statuses.
          </p>
        </div>
        
        {/* Eligibility Checks Table */}
        <Card>
          <CardHeader>
            <CardTitle>Eligibility Checks</CardTitle>
          </CardHeader>
          <CardContent>
            <EligibilityChecksTable />
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  )
}