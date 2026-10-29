import React from 'react'
import { Loader2 } from 'lucide-react'

export const LoadingState: React.FC = () => (
  <div className="flex flex-col items-center justify-center gap-3 py-12 text-slate-500">
    <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
    <span className="text-sm font-medium">Loading expense records...</span>
  </div>
)