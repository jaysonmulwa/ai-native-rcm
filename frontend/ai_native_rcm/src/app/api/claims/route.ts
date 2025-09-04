import { NextRequest, NextResponse } from 'next/server'
import { Claim } from '@/types/claims'

// Mock data - replace with actual database queries
const mockClaims: Claim[] = [
  {
    id: '1',
    claimNumber: 'CLM-2024-001',
    customerName: 'John Doe',
    dateSubmitted: '2024-01-15',
    amount: 2500.00,
    status: 'pending',
    description: 'Water damage to basement',
    assignedTo: 'Sarah Wilson'
  },
  {
    id: '2',
    claimNumber: 'CLM-2024-002',
    customerName: 'Jane Smith',
    dateSubmitted: '2024-01-14',
    amount: 4200.50,
    status: 'approved',
    description: 'Vehicle collision repair',
    assignedTo: 'Mike Johnson'
  },
  {
    id: '3',
    claimNumber: 'CLM-2024-003',
    customerName: 'Bob Wilson',
    dateSubmitted: '2024-01-13',
    amount: 850.75,
    status: 'rejected',
    description: 'Phone screen replacement',
    assignedTo: 'Emily Davis'
  },
  {
    id: '4',
    claimNumber: 'CLM-2024-004',
    customerName: 'Alice Johnson',
    dateSubmitted: '2024-01-12',
    amount: 1200.00,
    status: 'under_review',
    description: 'Medical expenses claim',
    assignedTo: 'David Brown'
  },
  {
    id: '5',
    claimNumber: 'CLM-2024-005',
    customerName: 'Charlie Brown',
    dateSubmitted: '2024-01-11',
    amount: 3400.25,
    status: 'processing',
    description: 'Home theft claim',
    assignedTo: 'Lisa Anderson'
  },
  {
    id: '6',
    claimNumber: 'CLM-2024-006',
    customerName: 'Diana Prince',
    dateSubmitted: '2024-01-10',
    amount: 5200.00,
    status: 'approved',
    description: 'Fire damage restoration',
    assignedTo: 'Tom Wilson'
  },
  {
    id: '7',
    claimNumber: 'CLM-2024-007',
    customerName: 'Frank Castle',
    dateSubmitted: '2024-01-09',
    amount: 750.00,
    status: 'pending',
    description: 'Laptop replacement',
    assignedTo: 'Sarah Wilson'
  },
  {
    id: '8',
    claimNumber: 'CLM-2024-008',
    customerName: 'Grace Lee',
    dateSubmitted: '2024-01-08',
    amount: 2800.90,
    status: 'under_review',
    description: 'Dental treatment expenses',
    assignedTo: 'Mike Johnson'
  }
]

export async function GET(request: NextRequest) {
  try {
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 500))
    
    const { searchParams } = new URL(request.url)
    const sortBy = searchParams.get('sortBy') || 'dateSubmitted'
    const sortDir = searchParams.get('sortDir') || 'desc'
    const status = searchParams.get('status')
    
    let filteredClaims = [...mockClaims]
    
    // Filter by status if provided
    if (status && status !== 'all') {
      filteredClaims = filteredClaims.filter(claim => claim.status === status)
    }
    
    // Sort claims
    filteredClaims.sort((a, b) => {
      const aValue = a[sortBy as keyof Claim]
      const bValue = b[sortBy as keyof Claim]
      
      if (typeof aValue === 'string' && typeof bValue === 'string') {
        return sortDir === 'asc' 
          ? aValue.localeCompare(bValue)
          : bValue.localeCompare(aValue)
      }
      
      if (typeof aValue === 'number' && typeof bValue === 'number') {
        return sortDir === 'asc' ? aValue - bValue : bValue - aValue
      }
      
      return 0
    })
    
    return NextResponse.json({
      claims: filteredClaims,
      total: filteredClaims.length
    })
    
  } catch (error) {
    console.error('Error fetching claims:', error)
    return NextResponse.json(
      { error: 'Failed to fetch claims' },
      { status: 500 }
    )
  }
}