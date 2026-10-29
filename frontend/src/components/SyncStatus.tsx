import { useEffect, useState } from 'react'
import { fetchSyncStatus } from '../services/api'

export const SyncStatus = () => {
  const [status, setStatus] = useState<'connected' | 'refreshing' | 'stale' | 'disconnected'>(
    'connected'
  )
  const [lastSync, setLastSync] = useState<string | null>(null)
  const [message, setMessage] = useState<string | undefined>()

  useEffect(() => {
    fetchSyncStatus().then((data) => {
      setStatus(data.status)
      setLastSync(data.lastSync)
      setMessage(data.message)
    })
  }, [])

  const statusLabels: Record<'connected' | 'refreshing' | 'stale' | 'disconnected', string> = {
    connected: 'Connected',
    refreshing: 'Refreshing',
    stale: 'Stale',
    disconnected: 'Disconnected',
  }

  const statusClasses: Record<'connected' | 'refreshing' | 'stale' | 'disconnected', string> = {
    connected: 'bg-green-100 text-green-800',
    refreshing: 'bg-blue-100 text-blue-800',
    stale: 'bg-amber-100 text-amber-800',
    disconnected: 'bg-red-100 text-red-800',
  }

  return (
    <div className="flex items-center gap-2">
      <span className={`px-2 py-1 rounded text-xs font-medium ${statusClasses[status]}`}>
        {statusLabels[status]}
      </span>
      {lastSync && (
        <span className="text-xs text-muted-foreground">
          Last sync: {lastSync}
        </span>
      )}
      {message && (
        <span className="text-xs text-muted-foreground mt-1">{message}</span>
      )}
    </div>
  )
}