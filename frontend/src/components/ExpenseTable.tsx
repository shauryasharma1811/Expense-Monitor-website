import type { ExpenseRecord } from '../types'

interface ExpenseTableProps {
  records: ExpenseRecord[]
  sortBy: 'date' | 'amount'
  sortOrder: 'asc' | 'desc'
  onSortChange: (col: 'date' | 'amount') => void
}

function SortIcon({ active, order }: { active: boolean; order: 'asc' | 'desc' }) {
  return (
    <span className={`ml-1 inline-block text-xs ${active ? 'text-blue-600' : 'text-slate-300'}`}>
      {order === 'asc' ? '↑' : '↓'}
    </span>
  )
}

const STATUS_CLASSES: Record<string, string> = {
  completed: 'bg-emerald-50 text-emerald-700 border border-emerald-200',
  pending:   'bg-amber-50 text-amber-700 border border-amber-200',
  failed:    'bg-red-50 text-red-700 border border-red-200',
}

export function ExpenseTable({ records, sortBy, sortOrder, onSortChange }: ExpenseTableProps) {
  const thBase =
    'px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-500 bg-slate-50 whitespace-nowrap'
  const thSortable = `${thBase} cursor-pointer select-none hover:text-slate-800 hover:bg-slate-100 transition-colors`

  return (
    <div className="overflow-x-auto rounded-xl border border-slate-200 bg-white shadow-sm">
      <table className="w-full text-sm text-left">
        <thead className="border-b border-slate-200">
          <tr>
            <th className={thBase}>Transaction ID</th>
            <th
              className={thSortable}
              onClick={() => onSortChange('date')}
              aria-sort={sortBy === 'date' ? (sortOrder === 'asc' ? 'ascending' : 'descending') : 'none'}
            >
              Date <SortIcon active={sortBy === 'date'} order={sortOrder} />
            </th>
            <th className={thBase}>Description</th>
            <th className={thBase}>Category</th>
            <th
              className={`${thSortable} text-right`}
              onClick={() => onSortChange('amount')}
              aria-sort={sortBy === 'amount' ? (sortOrder === 'asc' ? 'ascending' : 'descending') : 'none'}
            >
              Amount <SortIcon active={sortBy === 'amount'} order={sortOrder} />
            </th>
            <th className={thBase}>Currency</th>
            <th className={thBase}>Status</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100">
          {records.map((r) => (
            <tr key={r.id} className="hover:bg-slate-50 transition-colors">
              <td className="px-4 py-3 font-mono text-xs text-slate-500">{r.transactionId}</td>
              <td className="px-4 py-3 text-slate-700 whitespace-nowrap">{r.date}</td>
              <td className="px-4 py-3 text-slate-800 font-medium max-w-xs truncate">{r.description}</td>
              <td className="px-4 py-3 text-slate-600">{r.category}</td>
              <td className="px-4 py-3 text-right font-semibold text-slate-900 tabular-nums">
                {r.amount.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
              </td>
              <td className="px-4 py-3 text-slate-600 uppercase text-xs font-medium">{r.currency}</td>
              <td className="px-4 py-3">
                {r.status ? (
                  <span className={`inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full text-xs font-medium ${STATUS_CLASSES[r.status] ?? ''}`}>
                    <span className="w-1.5 h-1.5 rounded-full bg-current" />
                    {r.status.charAt(0).toUpperCase() + r.status.slice(1)}
                  </span>
                ) : (
                  <span className="text-slate-300">—</span>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
