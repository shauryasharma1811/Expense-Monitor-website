import React from 'react'
import { AlertTriangle } from 'lucide-react'

interface ErrorStateProps {
  message?: string;
}

export const ErrorState: React.FC<ErrorStateProps> = ({ message = 'Failed to load data.' }) => (
  <div className="flex flex-col items-center justify-center gap-3 py-12 text-red-600 bg-red-50 rounded-lg border border-red-100">
    <AlertTriangle className="w-8 h-8" />
    <div className="text-center">
      <p className="font-medium">Something went wrong</p>
      <p className="text-sm text-red-500">{message}</p>
    </div>
  </div>
)