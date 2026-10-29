# Expense Monitor - Frontend Deliverables & Status

## Implemented Features & Components

### Routes Created
- `/login`: Secure enterprise login page with corporate identity & access key inputs.
- `/dashboard`: Main financial expense monitoring dashboard (protected route).

### Reusable Components Created
- **AppLayout**: Main application wrapper with persistent top bar and secure footer.
- **TopBar**: Header showing application title, user role, real-time sync status indicator, and sign-out control.
- **SyncStatus**: Live connection state indicator (Connected, Refreshing, Stale, Disconnected) with last synchronization timestamp.
- **ReadOnlyIndicator**: Clear indicator ensuring users understand data is synchronized read-only from the backend.
- **ExpenseTable**: Comprehensive transaction table with columns for Transaction ID, Date, Description, Category, Amount, Currency, and Status. Supports sorting by Date and Amount.
- **ExpenseFilters**: Controls for searching by transaction ID or description, filtering by date range (From / To), and clearing filters.
- **Pagination**: Responsive page navigation controls.
- **LoadingState**: Clean loading spinner state.
- **EmptyState**: Informative empty state for zero-result queries.
- **ErrorState**: Graceful error handling state with retry guidance.

### Architecture & Security Rules Followed
- **TypeScript interfaces**: Defined in `src/types/index.ts` for API data (`ExpenseRecord`, `SyncStatusInfo`).
- **Separation of Concerns**: API service methods isolated in `src/services/api.ts`.
- **No Hardcoded Financial Records**: Data is fetched dynamically from the FastAPI backend endpoint (`/api/expenses`).
- **Secure Authentication**: Authentication state is handled via backend tokens/cookies without fake client-side security pretenses.
- **Environment Variables**: Public frontend configuration is accessed via `import.meta.env.VITE_API_BASE_URL`. Secrets are never exposed.

## Instructions to Run the Application
1. Install dependencies: `npm install`
2. Start development server: `npm run dev`
3. Build for production: `npm run build`
