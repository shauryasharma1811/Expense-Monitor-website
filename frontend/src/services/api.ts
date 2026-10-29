import type { ExpenseRecord, SyncStatusInfo } from '../types'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export async function fetchExpenses(
  page: number = 1,
  pageSize: number = 20,
  search?: string,
  dateFrom?: string,
  dateTo?: string,
  sortBy?: 'date' | 'amount',
  sortOrder?: 'asc' | 'desc'
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

  const response = await fetch(`${API_BASE_URL}/api/expenses?${params}`)

  if (!response.ok) {
    throw new Error(`Failed to fetch expenses: ${response.status}`)
  }

  return response.json()
}

export async function fetchSyncStatus(): Promise<SyncStatusInfo> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/sync-status`)

    if (!response.ok) {
      return { status: 'disconnected', lastSync: null }
    }

    return response.json()
  } catch {
    return { status: 'disconnected', lastSync: null }
  }
}