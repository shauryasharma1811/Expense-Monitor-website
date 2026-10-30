import { useState, useEffect, useCallback } from 'react'
import type { ExpenseRecord } from '../types'
import { fetchExpenses } from '../services/api'
import { ExpenseTable } from '../components/ExpenseTable'
import { ExpenseFilters } from '../components/ExpenseFilters'
import { Pagination } from '../components/Pagination'
import { LoadingState } from '../components/LoadingState'
import { EmptyState } from '../components/EmptyState'
import { ErrorState } from '../components/ErrorState'
import { SyncStatus } from '../components/SyncStatus'

const PAGE_SIZE = 20

export function DashboardPage() {
  const [records, setRecords] = useState<ExpenseRecord[]>([])
  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>(null)

  // Filters and state
  const [search, setSearch] = useState('')
  const [category, setCategory] = useState('')
  const [dateFrom, setDateFrom] = useState('')
  const [dateTo, setDateTo] = useState('')
  const [sortBy, setSortBy] = useState<'date' | 'amount'>('date')
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc')
  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const [totalCount, setTotalCount] = useState(0)

  const loadData = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await fetchExpenses(
        page,
        PAGE_SIZE,
        search || undefined,
        dateFrom || undefined,
        dateTo || undefined,
        sortBy,
        sortOrder,
        category || undefined
      )
      setRecords(response.data)
      setTotalPages(response.totalPages)
      setTotalCount(response.total)
    } catch (err: unknown) {
      setError(
        err instanceof Error
          ? err.message
          : 'An unexpected error occurred while fetching expense records.'
      )
    } finally {
      setLoading(false)
    }
  }, [page, search, category, dateFrom, dateTo, sortBy, sortOrder])

  useEffect(() => {
    loadData()
  }, [loadData])

  const handleSortChange = (column: 'date' | 'amount') => {
    if (sortBy === column) {
      setSortOrder((prev) => (prev === 'asc' ? 'desc' : 'asc'))
    } else {
      setSortBy(column)
      setSortOrder('desc')
    }
    setPage(1)
  }

  const handleClearFilters = () => {
    setSearch('')
    setCategory('')
    setDateFrom('')
    setDateTo('')
    setPage(1)
  }

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold tracking-tight text-slate-900">Expenses</h2>
          <p className="text-sm text-slate-500 mt-1">
            Read-only monitoring synchronized with primary accounts.
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-3">
          <SyncStatus />
          <span className="text-xs font-medium px-2.5 py-1 bg-slate-100 text-slate-700 rounded-md border border-slate-200">
            Total records: {totalCount}
          </span>
        </div>
      </div>

      <ExpenseFilters
        search={search}
        category={category}
        dateFrom={dateFrom}
        dateTo={dateTo}
        onSearchChange={(v) => {
          setSearch(v)
          setPage(1)
        }}
        onCategoryChange={(v) => {
          setCategory(v)
          setPage(1)
        }}
        onDateFromChange={(v) => {
          setDateFrom(v)
          setPage(1)
        }}
        onDateToChange={(v) => {
          setDateTo(v)
          setPage(1)
        }}
        onClear={handleClearFilters}
      />

      {loading ? (
        <LoadingState />
      ) : error ? (
        <ErrorState message={error} />
      ) : records.length === 0 ? (
        <EmptyState />
      ) : (
        <>
          <ExpenseTable
            records={records}
            sortBy={sortBy}
            sortOrder={sortOrder}
            onSortChange={handleSortChange}
          />
          <Pagination
            page={page}
            totalPages={totalPages}
            onPageChange={(p) => setPage(p)}
          />
        </>
      )}
    </div>
  )
}
