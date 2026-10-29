import React from 'react'
import { FileX } from 'lucide-react'

export const EmptyState: React.FC = () => (
  <div className="flex flex-col items-center justify-center gap-3 py-12 text-slate-400">
    <FileX className="w-10 h-10" />
    <div className="text-center">
      <p className="font-medium text-slate-500">No expenses found</p>
      <p className="text-sm">Try adjusting your filters or search criteria.</p>
    </div>
  </div>
)