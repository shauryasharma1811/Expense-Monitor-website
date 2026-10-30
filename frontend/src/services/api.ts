import type { ExpenseRecord, SyncStatusInfo } from '../types'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export const MOCK_EXPENSES: ExpenseRecord[] = [
  {
    id: 'exp-1',
    transactionId: 'TXN-984321',
    date: '2026-10-25',
    description: 'AWS Cloud Hosting Services',
    category: 'Infrastructure',
    amount: 1450.0,
    currency: 'USD',
    status: 'completed',
  },
  {
    id: 'exp-2',
    transactionId: 'TXN-984322',
    date: '2026-10-24',
    description: 'Datadog Monitoring License',
    category: 'Software',
    amount: 320.5,
    currency: 'USD',
    status: 'completed',
  },
  {
    id: 'exp-3',
    transactionId: 'TXN-984323',
    date: '2026-10-23',
    description: 'Office Supplies & Equipment',
    category: 'Operations',
    amount: 185.2,
    currency: 'USD',
    status: 'completed',
  },
  {
    id: 'exp-4',
    transactionId: 'TXN-984324',
    date: '2026-10-22',
    description: 'Google Workspace Subscriptions',
    category: 'Software',
    amount: 720.0,
    currency: 'USD',
    status: 'completed',
  },
  {
    id: 'exp-5',
    transactionId: 'TXN-984325',
    date: '2026-10-21',
    description: 'Client Lunch Meeting - Q3 Review',
    category: 'Meals & Entertainment',
    amount: 95.4,
    currency: 'USD',
    status: 'completed',
  },
  {
    id: 'exp-6',
    transactionId: 'TXN-984326',
    date: '2026-10-20',
    description: 'GitHub Enterprise Team Plan',
    category: 'Software',
    amount: 210.0,
    currency: 'USD',
    status: 'completed',
  },
  {
    id: 'exp-7',
    transactionId: 'TXN-984327',
    date: '2026-10-18',
    description: 'Figma Enterprise Design Seats',
    category: 'Software',
    amount: 150.0,
    currency: 'USD',
    status: 'completed',
  },
  {
    id: 'exp-8',
    transactionId: 'TXN-984328',
    date: '2026-10-15',
    description: 'Conference Travel & Lodging',
    category: 'Travel',
    amount: 890.75,
    currency: 'USD',
    status: 'pending',
  },
  {
    id: 'exp-9',
    transactionId: 'TXN-984329',
    date: '2026-10-14',
    description: 'Ergonomic Standing Desks',
    category: 'Operations',
    amount: 1200.0,
    currency: 'USD',
    status: 'completed',
  },
  {
    id: 'exp-10',
    transactionId: 'TXN-984330',
    date: '2026-10-12',
    description: 'Slack Enterprise Grid License',
    category: 'Software',
    amount: 450.0,
    currency: 'USD',
    status: 'completed',
  },
  {
    id: 'exp-11',
    transactionId: 'TXN-984331',
    date: '2026-10-10',
    description: 'Uber Business Ground Transportation',
    category: 'Travel',
    amount: 45.6,
    currency: 'USD',
    status: 'completed',
  },
  {
    id: 'exp-12',
    transactionId: 'TXN-984332',
    date: '2026-10-08',
    description: 'Security Audit & Pen Testing',
    category: 'Legal & Professional',
    amount: 3500.0,
    currency: 'USD',
    status: 'completed',
  },
  {
    id: 'exp-13',
    transactionId: 'TXN-984333',
    date: '2026-10-05',
    description: 'Internet Fiber Dedicated Connection',
    category: 'Infrastructure',
    amount: 250.0,
    currency: 'USD',
    status: 'completed',
  },
  {
    id: 'exp-14',
    transactionId: 'TXN-984334',
    date: '2026-10-03',
    description: 'Team Dinner Celebration',
    category: 'Meals & Entertainment',
    amount: 340.5,
    currency: 'USD',
    status: 'completed',
  },
  {
    id: 'exp-15',
    transactionId: 'TXN-984335',
    date: '2026-10-01',
    description: 'Quarterly Accounting Audit Services',
    category: 'Legal & Professional',
    amount: 1800.0,
    currency: 'USD',
    status: 'completed',
  },
  {
    id: 'exp-16',
    transactionId: 'TXN-984336',
    date: '2026-09-29',
    description: 'Stripe Payment Processing Fees',
    category: 'Operations',
    amount: 112.4,
    currency: 'USD',
    status: 'completed',
  },
  {
    id: 'exp-17',
    transactionId: 'TXN-984337',
    date: '2026-09-27',
    description: 'Zoom Enterprise Video Conference',
    category: 'Software',
    amount: 199.0,
    currency: 'USD',
    status: 'completed',
  },
  {
    id: 'exp-18',
    transactionId: 'TXN-984338',
    date: '2026-09-25',
    description: 'Airport Parking & Tolls',
    category: 'Travel',
    amount: 68.0,
    currency: 'USD',
    status: 'completed',
  },
  {
    id: 'exp-19',
    transactionId: 'TXN-984339',
    date: '2026-09-22',
    description: 'Postgres Managed Database Cluster',
    category: 'Infrastructure',
    amount: 540.0,
    currency: 'USD',
    status: 'completed',
  },
  {
    id: 'exp-20',
    transactionId: 'TXN-984340',
    date: '2026-09-20',
    description: 'Notion Team Workspace Subscription',
    category: 'Software',
    amount: 120.0,
    currency: 'USD',
    status: 'completed',
  },
  {
    id: 'exp-21',
    transactionId: 'TXN-984341',
    date: '2026-09-18',
    description: 'Hardware Key Fobs for 2FA',
    category: 'Operations',
    amount: 290.0,
    currency: 'USD',
    status: 'completed',
  },
  {
    id: 'exp-22',
    transactionId: 'TXN-984342',
    date: '2026-09-15',
    description: '1Password Team Passwords Vault',
    category: 'Software',
    amount: 80.0,
    currency: 'USD',
    status: 'completed',
  },
]

export async function fetchExpenses(
  page: number = 1,
  pageSize: number = 20,
  search?: string,
  dateFrom?: string,
  dateTo?: string,
  sortBy?: 'date' | 'amount',
  sortOrder?: 'asc' | 'desc',
  category?: string
): Promise<{
  data: ExpenseRecord[]
  total: number
  totalPages: number
}> {
  const params = new URLSearchParams({
    page: page.toString(),
    page_size: pageSize.toString(),
  })

  if (search) params.append('search', search)
  if (dateFrom) params.append('date_from', dateFrom)
  if (dateTo) params.append('date_to', dateTo)
  if (sortBy) params.append('sort_by', sortBy)
  if (sortOrder) params.append('sort_order', sortOrder)
  if (category) params.append('category', category)

  try {
    const token = localStorage.getItem('token')
    const headers: Record<string, string> = {}
    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }

    const response = await fetch(`${API_BASE_URL}/api/expenses?${params}`, {
      headers,
    })

    if (response.ok) {
      return await response.json()
    }
  } catch {
    // Backend unavailable or erroring, fall back to mock data
  }

  // Fallback filtering on mock data
  let filtered = [...MOCK_EXPENSES]

  if (search) {
    const q = search.toLowerCase()
    filtered = filtered.filter(
      (item) =>
        item.description.toLowerCase().includes(q) ||
        item.transactionId.toLowerCase().includes(q)
    )
  }

  if (category) {
    filtered = filtered.filter((item) => item.category === category)
  }

  if (dateFrom) {
    filtered = filtered.filter((item) => item.date >= dateFrom)
  }

  if (dateTo) {
    filtered = filtered.filter((item) => item.date <= dateTo)
  }

  if (sortBy) {
    filtered.sort((a, b) => {
      let comparison = 0
      if (sortBy === 'date') {
        comparison = a.date.localeCompare(b.date)
      } else if (sortBy === 'amount') {
        comparison = a.amount - b.amount
      }
      return sortOrder === 'asc' ? comparison : -comparison
    })
  }

  const total = filtered.length
  const totalPages = Math.max(1, Math.ceil(total / pageSize))
  const startIndex = (page - 1) * pageSize
  const paginatedData = filtered.slice(startIndex, startIndex + pageSize)

  return {
    data: paginatedData,
    total,
    totalPages,
  }
}

export async function fetchSyncStatus(): Promise<SyncStatusInfo> {
  try {
    const token = localStorage.getItem('token')
    const headers: Record<string, string> = {}
    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }

    const response = await fetch(`${API_BASE_URL}/api/sync-status`, { headers })

    if (response.ok) {
      return await response.json()
    }
  } catch {
    // Backend offline / not reachable
  }

  return {
    status: 'connected',
    lastSync: '2026-10-30 14:00 UTC',
    message: 'Local mock sync active (read-only mode)',
  }
}
