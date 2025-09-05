import { NextRequest, NextResponse } from 'next/server'
import { ScrubbedClaim } from '@/types/scrubbed_claims'

const BACKEND_API_URL = "http://84.247.129.35:9000"

export async function GET(request: NextRequest) {
  try {
    // Fetch ALL scrubbed claims from backend
    const response = await fetch(`${BACKEND_API_URL}/claims_scrubbing`, {
      headers: {
        'Authorization': `Bearer ${process.env.API_TOKEN}`,
        'Content-Type': 'application/json',
      },
    })

    if (!response.ok) {
      throw new Error(`Backend API responded with ${response.status}`)
    }
    
    const data = await response.json()

    console.log("Fetched scrubbed claims from backend:", data)
    
    let scrubbedClaims: ScrubbedClaim[] = data.scrubbedClaims || data

    console.log("Initial scrubbed claims:", scrubbedClaims)
    
    return NextResponse.json({
      scrubbedClaims,
      total: scrubbedClaims.length
    })
    
  } catch (error) {
    console.error('Error fetching scrubbed claims:', error)
    return NextResponse.json(
      { error: 'Failed to fetch scrubbed claims from backend' },
      { status: 500 }
    )
  }
}
