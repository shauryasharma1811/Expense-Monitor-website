import { Search, Calendar, Tag } from 'lucide-react'

interface ExpenseFiltersProps {
  search: string
  dateFrom: string
  dateTo: string
  category?: string
  categories?: string[]
  onSearchChange: (v: string) => void
  onDateFromChange: (v: string) => void
  onDateToChange: (v: string) => void
  onCategoryChange?: (v: string) => void
  onClear: () => void
}

const inputClass =
  'w-full py-2 rounded-lg border border-slate-300 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/30 focus:border-blue-500 transition-colors bg-white text-slate-900 placeholder:text-slate-400'

export function ExpenseFilters({
  search,
  dateFrom,
  dateTo,
  category = '',
  categories = [
    'Infrastructure',
    'Software',
    'Operations',
    'Meals & Entertainment',
    'Travel',
    'Legal & Professional',
  ],
  onSearchChange,
  onDateFromChange,
  onDateToChange,
  onCategoryChange,
  onClear,
}: ExpenseFiltersProps) {
  const hasFilters = search || dateFrom || dateTo || category

  return (
    <div className="bg-white border border-slate-200 rounded-xl p-4 shadow-sm">
      <div className="flex flex-wrap gap-3 items-end">
        <div className="flex-1 min-w-[220px]">
          <label htmlFor="search" className="block text-xs font-semibold text-slate-500 mb-1.5 uppercase tracking-wide">
            Search
          </label>
          <div className="relative">
            <Search className="absolute left-2.5 top-2.5 w-4 h-4 text-slate-400 pointer-events-none" />
            <input
              id="search"
              type="text"
              value={search}
              onChange={(e) => onSearchChange(e.target.value)}
              placeholder="Transaction ID or description…"
              className={`${inputClass} pl-9 pr-3`}
            />
          </div>
        </div>

        {onCategoryChange && (
          <div className="min-w-[180px]">
            <label htmlFor="category" className="block text-xs font-semibold text-slate-500 mb-1.5 uppercase tracking-wide">
              Category
            </label>
            <div className="relative">
              <Tag className="absolute left-2.5 top-2.5 w-4 h-4 text-slate-400 pointer-events-none" />
              <select
                id="category"
                value={category}
                onChange={(e) => onCategoryChange(e.target.value)}
                className={`${inputClass} pl-9 pr-3 appearance-none bg-no-repeat`}
              >
                <option value="">All Categories</option>
                {categories.map((cat) => (
                  <option key={cat} value={cat}>
                    {cat}
                  </option>
                ))}
              </select>
            </div>
          </div>
        )}

        <div>
          <label htmlFor="dateFrom" className="block text-xs font-semibold text-slate-500 mb-1.5 uppercase tracking-wide">
            From
          </label>
          <div className="relative">
            <Calendar className="absolute left-2.5 top-2.5 w-4 h-4 text-slate-400 pointer-events-none" />
            <input
              id="dateFrom"
              type="date"
              value={dateFrom}
              onChange={(e) => onDateFromChange(e.target.value)}
              max={dateTo || undefined}
              className={`${inputClass} pl-9 pr-3`}
            />
          </div>
        </div>

        <div>
          <label htmlFor="dateTo" className="block text-xs font-semibold text-slate-500 mb-1.5 uppercase tracking-wide">
            To
          </label>
          <div className="relative">
            <Calendar className="absolute left-2.5 top-2.5 w-4 h-4 text-slate-400 pointer-events-none" />
            <input
              id="dateTo"
              type="date"
              value={dateTo}
              onChange={(e) => onDateToChange(e.target.value)}
              min={dateFrom || undefined}
              className={`${inputClass} pl-9 pr-3`}
            />
          </div>
        </div>

        {hasFilters && (
          <button
            onClick={onClear}
            className="py-2 px-4 text-sm rounded-lg border border-slate-300 text-slate-600 hover:bg-slate-50 hover:border-slate-400 transition-colors"
          >
            Clear filters
          </button>
        )}
      </div>
    </div>
  )
}
