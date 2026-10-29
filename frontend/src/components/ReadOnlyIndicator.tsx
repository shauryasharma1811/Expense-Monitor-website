import React from 'react'
import { ShieldCheck } from 'lucide-react'

export const ReadOnlyIndicator: React.FC = () => (
  <div className="flex items-center gap-2 bg-slate-50 border border-slate-200 rounded-md px-3 py-2 text-sm text-slate-600">
    <ShieldCheck className="w-4 h-4 text-blue-600" />
    <span className="font-medium">Read-only view</span>
    <span className="text-slate-400">— data is synchronized from the backend and cannot be edited here</span>
  </div>
)