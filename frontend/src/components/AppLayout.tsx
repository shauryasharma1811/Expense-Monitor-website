import React from 'react'
import { TopBar } from './TopBar'
import { ReadOnlyIndicator } from './ReadOnlyIndicator'

interface AppLayoutProps {
  children: React.ReactNode;
}

export const AppLayout: React.FC<AppLayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen bg-slate-50 flex flex-col text-slate-900 antialiased">
      <TopBar />
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 flex flex-col gap-6">
        <ReadOnlyIndicator />
        {children}
      </main>
      <footer className="bg-white border-t border-slate-200 py-4 px-6 text-center text-xs text-slate-500">
        Expense Monitor Enterprise Financial Dashboard &copy; 2026. All rights reserved. Secure Read-Only Access.
      </footer>
    </div>
  )
}
