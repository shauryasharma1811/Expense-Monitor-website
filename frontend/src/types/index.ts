export interface ExpenseRecord {
  id: string;
  transactionId: string;
  date: string;
  description: string;
  category: string;
  amount: number;
  currency: string;
  status?: 'completed' | 'pending' | 'failed';
}

export interface SyncStatusInfo {
  status: 'connected' | 'refreshing' | 'stale' | 'disconnected';
  lastSync: string | null;
  message?: string;
}
