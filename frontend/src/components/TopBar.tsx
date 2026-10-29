import React from 'react'
import { SyncStatus } from './SyncStatus'
import { LogOut, User } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

export const TopBar: React.FC = () => {
  const navigate = useNavigate()

  const handleLogout = () => {
    localStorage.removeItem('isAuthenticated')
    navigate('/login')
  }

  return (
    <header className="bg-white border-b border-slate-200 px-6 py-4 flex items-center justify-between shadow-sm">
      <div className="flex items-center gap-4">
        <h1 className="text-xl font-bold tracking-tight text-slate-900 m-0">Expense Monitor</h1>
        <div className="h-5 w-px bg-slate-200" />
        <SyncStatus />
      </div>

      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2 text-sm text-slate-600 bg-slate-50 px-3 py-1.5 rounded-full border border-slate-200">
          <User className="w-4 h-4 text-slate-500" />
          <span className="font-medium">Auditor</span>
        </div>
        <button
          onClick={handleLogout}
          className="flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium text-slate-700 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors border border-slate-200 hover:border-red-200"
          title="Sign out"
        >
          <LogOut className="w-4 h-4" />
          <span>Sign out</span>
        </button>
      </div>
    </header>
  )
}
